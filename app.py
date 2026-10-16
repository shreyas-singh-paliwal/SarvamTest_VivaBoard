import os, json, re
from flask import Flask, request, jsonify, send_from_directory
from sarvamai import SarvamAI

app = Flask(__name__, static_folder="static")
API_KEY = os.getenv("SARVAM_API_KEY")
client = SarvamAI(api_subscription_key=API_KEY) if API_KEY else None

@app.get("/")
def index():
    return send_from_directory("static", "index.html")

@app.post("/api/transcribe")
def transcribe():
    if not client:
        return jsonify({"error": "SARVAM_API_KEY is not set. Add it to your environment and restart the app."}), 503
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received."}), 400
    audio = request.files["audio"]
    try:
        # Saaras v4 supports technical keyterms to help recognition.
        result = client.speech_to_text.transcribe(
            file=audio,
            model="saaras:v4",
            language_code="en-IN",
            keyterms=[
                "Boolean algebra", "Karnaugh map", "K-map", "minterm", "maxterm",
                "multiplexer", "demultiplexer", "flip-flop", "De Morgan's law",
                "AND gate", "OR gate", "XOR gate", "complement", "implicant"
            ]
        )
        return jsonify({"transcript": getattr(result, "transcript", str(result))})
    except Exception as e:
        return jsonify({"error": f"Sarvam transcription failed: {e}"}), 502

@app.post("/api/structure")
def structure():
    if not client:
        return jsonify({"error": "SARVAM_API_KEY is not set. Add it to your environment and restart the app."}), 503
    data = request.get_json(silent=True) or {}
    transcript = (data.get("transcript") or "").strip()
    if not transcript:
        return jsonify({"error": "Transcript is empty."}), 400

    prompt = f"""
You are VivaBoard, an assistant for a Digital Logic / Digital Circuits viva.
Convert the student's spoken explanation into a structured whiteboard state.
Do NOT invent what the student said. If an expression is ambiguous, mark it for review.
Return ONLY valid JSON with this schema:
{{
  "topic": "short topic label",
  "cleaned_transcript": "lightly punctuated transcript, preserve meaning",
  "concepts": ["concepts explicitly mentioned"],
  "expressions": [{{"spoken_form":"...", "latex":"...", "confidence":"high|medium|low", "needs_review":true}}],
  "steps": [{{"title":"...", "content":"...", "status":"stated|inferred|needs_review"}}],
  "truth_table": {{"variables":["A","B"], "rows":[{{"A":0,"B":0,"Y":0}}], "needs_review":true}},
  "follow_up_questions": ["one useful viva follow-up"],
  "examiner_notes": ["neutral observation, not an unsupported grade"],
  "uncertainties": ["ambiguous terms or assumptions"]
}}
Only populate a truth table when the transcript clearly specifies enough information to do so. Otherwise use empty variables and rows and explain the uncertainty. Never claim a result is mathematically verified; this prototype does not run a formal solver.
Student transcript:
{transcript}
"""
    try:
        result = client.chat.completions(
            model="sarvam-105b",
            messages=[
                {"role": "system", "content": "Return valid JSON only. No markdown fences."},
                {"role": "user", "content": prompt}
            ],
        )
        content = result.choices[0].message.content
        # Handle occasional fenced JSON responses defensively.
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.I)
        parsed = json.loads(content)
        return jsonify(parsed)
    except Exception as e:
        return jsonify({"error": f"Structuring failed: {e}"}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=True)
