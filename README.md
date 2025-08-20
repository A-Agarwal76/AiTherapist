## Depression Prediction and AI Therapist

This repository contains two Streamlit applications and one training script:

- AI Therapist app (`audin.py`): Voice-based assistant that transcribes speech, generates a concise, supportive response using a Gemini LLM-compatible API, and speaks the response back.
- Depression Prediction App (`depress.py`): Predicts whether a user is at risk of depression using a pre-trained RandomForest model, and can optionally send an email alert.
- Model Training (`dsp_pro.py`): Trains the RandomForest model and saves the model and label encoders.

Important: These tools are for educational and assistive purposes only and are not a substitute for professional mental health care.

### Features
- Speech-to-Text and Text-to-Speech via Sarvam.ai APIs
- LLM responses via Google Gemini (OpenAI SDK-compatible endpoint)
- Depression prediction using a RandomForest classifier
- Optional email alert when risk is detected
- Configuration via environment variables (no secrets committed)

---

## Getting Started

### Prerequisites
- Python 3.9+ recommended
- Windows PowerShell (instructions below use PowerShell)

### Create and activate a virtual environment
Windows (PowerShell):
```powershell
cd path
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux (bash or zsh):
```bash
cd path
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```powershell
pip install streamlit requests python-dotenv openai pandas scikit-learn joblib
```

If you plan to train the model (`dsp_pro.py`), ensure `pandas`, `scikit-learn`, and `joblib` are installed (included above).

---

## Configuration

Create a `.env` file in the project root with the following variables. Do NOT commit this file.

```ini
# Sarvam.ai API key (required for audin.py)
SARVAM_SUBSCRIPTION_KEY=

# Gemini-compatible API key (required for audin.py)
GEMINI_API_KEY=

# Paths (set to your actual locations; defaults shown)
DATA_PATH=dsp_pro.csv            # For dsp_pro.py
SAVE_DIRECTORY=.                 # For dsp_pro.py and depress.py (where model/encoders are stored)

# SMTP settings for email alerts (used by depress.py)
SMTP_SENDER_EMAIL=
SMTP_SENDER_PASSWORD=            # App password recommended
SMTP_RECIPIENT_EMAIL=
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

Security
- Keep `.env` out of version control (already ignored by `.gitignore`).
- Rotate any keys that were previously committed.

---

## Data and Models
- Training data file: `dsp_pro.csv` (place it in the project root or set `DATA_PATH`)
- Trained artifacts (default names used by `dsp_pro.py`):
  - `random_forest_model69.joblib`
  - `label_encoders69.joblib`
- The prediction app (`depress.py`) expects files named:
  - `random_forest_model.joblib`
  - `label_encoders.joblib`

You can rename the trained files or adjust `depress.py` to point to the `69`-suffixed files, or re-save them during training with the expected names. Place them in `SAVE_DIRECTORY`.

---

## How to Run

### 1) Train the model (optional)
```powershell
python dsp_pro.py
```
This reads `DATA_PATH`, trains a RandomForest classifier, and saves the model and encoders to `SAVE_DIRECTORY`.

### 2) Run the Depression Prediction app
Ensure `SAVE_DIRECTORY` contains `random_forest_model.joblib` and `label_encoders.joblib`.
```powershell
streamlit run depress.py
```
Optional: Set SMTP variables in `.env` to enable email alerts when the result is "Depressed".

### 3) Run the AI Therapist app
Requires `SARVAM_SUBSCRIPTION_KEY` and `GEMINI_API_KEY` in `.env`.
```powershell
streamlit run audin.py
```

---

## Troubleshooting
- Missing environment variables: Ensure `.env` exists and you restarted the terminal or re-activated the venv.
- Model files not found: Confirm `SAVE_DIRECTORY` points to the folder that contains the `.joblib` files expected by `depress.py`.
- SMTP auth errors: Use an app password and correct `SMTP_HOST`/`SMTP_PORT`. Some providers require enabling SMTP or using OAuth.
- Audio issues in `audin.py`: Verify your microphone permissions and that Sarvam.ai keys are valid. Check API quotas and response status codes in the terminal.

---

## Project Structure
```
MiniProject/
  audin.py                # AI Therapist Streamlit app (STT/LLM/TTS)
  depress.py              # Depression prediction Streamlit app (optional email alerts)
  dsp_pro.py              # Model training script
  dsp_pro.csv             # Example dataset (not required if DATA_PATH points elsewhere)
  random_forest_model.joblib        # Expected by depress.py (place in SAVE_DIRECTORY)
  label_encoders.joblib             # Expected by depress.py (place in SAVE_DIRECTORY)
  random_forest_model69.joblib      # Produced by dsp_pro.py (default)
  label_encoders69.joblib           # Produced by dsp_pro.py (default)
  .gitignore
```

---

## Notes
- This project uses the OpenAI SDK pointed to a Gemini-compatible endpoint. Ensure your `GEMINI_API_KEY` corresponds to that service.
- Do not use these tools as a replacement for clinical assessment. Always seek professional help when needed.


