"""
Clickbait detection stub.
Developer should add model and return a formatted string.
Provide function: is_clickbait(headline_text) -> str ("Yes" or "No")
"""

import os
import joblib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "..", "models")

MODEL_PATH = os.path.join(MODELS_DIR, "clickbait_model.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "clickbait_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def is_clickbait(headline_text: str) -> str:
    """
    Predict if a given headline is clickbait or not.

    Args:
        headline_text (str): The headline to classify.

    Returns:
        str: "Yes" if clickbait, "No" otherwise.
    """
    features = vectorizer.transform([headline_text])
    prediction = model.predict(features)[0]
    return "Yes" if prediction == 1 else "No"
