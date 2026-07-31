# CardioPredict AI

AI-powered heart failure risk prediction — a Flask app I built around a
Random Forest model as a portfolio project.

Give it a patient's age, a few lifestyle/condition flags, and some recent
blood work, and it returns a High/Low risk prediction. Nothing fancy under
the hood — the interesting part was less the model itself and more turning
it into something that feels like a real, usable app instead of a Jupyter
notebook.

> ⚠️ **Not a real medical tool.** Trained on ~300 records. Please don't use
> this for actual health decisions — see an actual doctor for that.

---

## Overview

Given twelve clinical parameters (age, blood test results, and existing
conditions), the app returns a **High Risk** or **Low Risk** prediction
along with the model's confidence, plain-language recommendations, and
details about how the prediction was generated.

The underlying model is a `RandomForestClassifier` trained on the
[Heart Failure Clinical Records dataset](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records),
a public dataset of 299 follow-up records for patients who experienced
heart failure.

## Features

- **Clean clinical UI** — a two-card intake form (Patient Information /
  Clinical Measurements) with dropdown and pill-style inputs instead of
  raw `0`/`1` fields
- **Client- and server-side validation** — realistic min/max ranges per
  field, friendly inline error messages, and defensive handling on the
  backend if something still slips through
- **Readable results** — a risk badge, plain-language explanation, and a
  model confidence meter instead of a raw `Prediction: 1`
- **Context-aware recommendations** — different guidance shown for
  high-risk vs. low-risk results
- **Model transparency panel** — algorithm name, dataset, feature count,
  and training sample count, read directly from the model and dataset at
  startup
- **Fully responsive** — desktop, laptop, tablet, and mobile layouts
- **Deployment-ready** — `Procfile`, `requirements.txt`, and a
  `PORT`-aware entry point for Render (or any Heroku-style host)

## Screenshots

> Add screenshots of the landing page and result page here once deployed,
> e.g.:
>
> `docs/screenshot-home.png`
> `docs/screenshot-result.png`

## Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Backend    | Flask (Python)                       |
| ML         | scikit-learn (`RandomForestClassifier`) |
| Data       | pandas, NumPy                        |
| Frontend   | HTML5, CSS3, vanilla JavaScript      |
| Deployment | Gunicorn + Render                    |

No frontend frameworks (React, Vue) or CSS frameworks (Bootstrap,
Tailwind) are used — the UI is hand-built.

## Folder Structure

```
cardiopredict-ai/
├── app.py                 # Flask application and prediction route
├── train_model.py         # Original training script (model.pkl source)
├── model.pkl              # Trained RandomForestClassifier
├── dataset.csv            # Heart Failure Clinical Records dataset
├── requirements.txt       # Python dependencies
├── Procfile                # Render/Heroku process definition
├── .gitignore
├── LICENSE
├── README.md
├── templates/
│   ├── index.html          # Landing page + intake form
│   └── result.html         # Prediction result page
└── static/
    ├── style.css           # All application styling
    └── script.js           # Client-side form validation
```

## How It Works

1. The user fills out the intake form across two sections: **Patient
   Information** (age, gender, anaemia, diabetes, smoking, high blood
   pressure) and **Clinical Measurements** (CPK enzyme, ejection
   fraction, platelets, serum creatinine, serum sodium, follow-up
   period).
2. On submit, `app.py` reads each field **by name** (not by form order),
   assembles them into a pandas DataFrame with the same column names the
   model was trained on, and calls `model.predict()`.
3. The result page renders a risk badge, an explanation, a confidence
   score (if the model supports `predict_proba`), and recommendations
   tailored to the outcome.

The model, dataset, and training pipeline (`train_model.py`) are
unchanged from the original project — only the surrounding application
was rebuilt.

## Installation

```bash
# Grab the project folder, then from inside it:
cd cardiopredict-ai

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at `http://127.0.0.1:5000`.

### Retraining the model (optional)

The trained model is already included as `model.pkl`. To retrain it from
`dataset.csv`:

```bash
python train_model.py
```

## Deployment (Render)

1. Push the project to a Git repository (Render deploys from a connected repo).
2. In Render, create a new **Web Service** and connect the repository.
3. Set the build command:
   ```
   pip install -r requirements.txt
   ```
4. Set the start command (already defined in `Procfile`):
   ```
   gunicorn app:app
   ```
5. Render automatically provides a `PORT` environment variable, which
   `app.py` reads on startup — no extra configuration needed.

## Things I'd Still Like to Do

- [ ] Actual tests — right now I've only checked it manually
- [ ] Show *why* the model made a prediction (SHAP values or similar),
      instead of just the number
- [ ] A JSON API route so this isn't only usable through the form
- [ ] Report the model's real accuracy/precision/recall somewhere instead
      of just "trust me"
- [ ] Probably retrain on a bigger dataset if I find one — 299 rows is
      thin for anything beyond a demo

## License

This project is licensed under the [MIT License](LICENSE).

---

*Built as a portfolio project. Not intended for clinical use.*
