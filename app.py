"""
CardioPredict AI — Flask backend

Loads the trained RandomForest model (from train_model.py, on the Heart
Failure Clinical Records dataset) and serves the intake form + prediction.

Didn't touch the model or the training pipeline. Main thing I fixed here
was that the original version read form values by position
(request.form.values()), which breaks silently if the fields ever get
reordered in the HTML. Now it reads each field by name instead, so that
can't happen.
"""

import csv
import os
import pickle

import pandas as pd
from flask import Flask, render_template, request

# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

MODEL_NAME = type(model).__name__

# Row count is read once at startup purely for the "Model Information"
# panel in the UI — it does not affect predictions in any way.
try:
    with open(DATASET_PATH, newline="") as f:
        SAMPLE_COUNT = sum(1 for _ in csv.reader(f)) - 1  # minus header row
except OSError:
    SAMPLE_COUNT = None

# The model was trained on these columns, in this exact order
# (see train_model.py: X = df.drop("DEATH_EVENT", axis=1)).
# Keeping this list explicit means the form can never accidentally
# submit fields in the wrong order.
FEATURE_ORDER = [
    "age",
    "anaemia",
    "creatinine_phosphokinase",
    "diabetes",
    "ejection_fraction",
    "high_blood_pressure",
    "platelets",
    "serum_creatinine",
    "serum_sodium",
    "sex",
    "smoking",
    "time",
]

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

def model_info():
    """Shared context for the 'Model Information' panel shown on both pages."""
    return {
        "model_name": MODEL_NAME,
        "feature_count": len(FEATURE_ORDER),
        "sample_count": SAMPLE_COUNT,
    }


@app.route("/")
def home():
    """Landing page with the patient intake form."""
    return render_template("index.html", **model_info())


@app.route("/predict", methods=["POST"])
def predict():
    """
    Reads the submitted clinical parameters, runs them through the
    existing trained model, and renders the result page.
    """
    try:
        # Pull each field explicitly by name, in the order the model expects.
        # Building a DataFrame (rather than a bare array) matches how the
        # model was trained (see train_model.py), so scikit-learn sees the
        # same column names it was fit on.
        values = {field: [float(request.form[field])] for field in FEATURE_ORDER}
        input_data = pd.DataFrame(values, columns=FEATURE_ORDER)

        prediction = int(model.predict(input_data)[0])

        # If the model supports probability estimates, surface a confidence
        # score for the UI. Falls back gracefully if it doesn't.
        confidence = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0]
            confidence = round(float(proba[prediction]) * 100, 1)

        return render_template(
            "result.html",
            prediction=prediction,
            confidence=confidence,
            patient={field: request.form[field] for field in FEATURE_ORDER},
            **model_info(),
        )

    except (KeyError, ValueError):
        # Missing field or a non-numeric value was submitted.
        return render_template(
            "index.html",
            error="Please check your entries — one or more fields are "
                  "missing or contain an invalid value.",
            **model_info(),
        )
    except Exception as exc:  # pragma: no cover - defensive fallback
        return render_template(
            "index.html",
            error=f"Something went wrong while generating a prediction: {exc}",
            **model_info(),
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
