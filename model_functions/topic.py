"""
Topic classification stub. Team Lead should replace with real model loading.
Provide function: predict_topic(text) -> str
"""

import os
import joblib

MODEL_PATH = os.path.join('models', 'topic_model.pkl')
VECTORIZER_PATH = os.path.join('models', 'topic_vectorizer.pkl')

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_topic(text: str) -> str:
    # Returns a news topic prediction for the given text
    if not text or not text.strip():
        return "No text provided"
    x = vectorizer.transform([text])
    prediction = model.predict(x)[0]
    return prediction

