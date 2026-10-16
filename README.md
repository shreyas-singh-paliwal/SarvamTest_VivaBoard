# VivaBoard — 30-minute prototype

A small voice-to-whiteboard prototype for Digital Circuits viva practice:
- Record a short answer in the browser.
- Transcribe it with Sarvam Saaras v4.
- Turn the transcript into structured concepts, equations, steps, and follow-up questions using Sarvam chat completion.
- Review/edit the transcript before structuring it.

## Setup

Requires Python 3.9+ and a Sarvam API key.

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SARVAM_API_KEY="YOUR_KEY"
python app.py
```

### Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SARVAM_API_KEY="YOUR_KEY"
python app.py
```

Open http://127.0.0.1:5000 and allow microphone access.

## Demo flow
1. Click **Record answer**, explain a Boolean simplification for 10–20 seconds, then click **Stop**.
2. Click **Transcribe with Sarvam**.
3. Correct any technical-term transcription errors in the editable transcript.
4. Click **Build whiteboard** to create structured notes.

## Important limitations
- This is a prototype, not an autonomous grading system.
- Sarvam API calls require an API key and may incur usage charges under your account.
- Audio is sent to Sarvam for transcription. Don't record real student evaluations without consent and appropriate data handling.
- Truth tables and equations are AI-generated suggestions, not formally verified results. A production version should add a symbolic Boolean-equivalence checker and ask for confirmation when spoken notation is ambiguous.
- Browser microphone recording typically works on localhost or HTTPS.
