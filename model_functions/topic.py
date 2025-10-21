"""
Topic classification stub. Team Lead should replace with real model loading.
Provide function: predict_topic(text) -> str
"""

import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'topic_model.pkl')


def predict_topic(text: str) -> str:
    """Return predicted topic as string. Current stub returns a placeholder.
    Replace this with actual model loading and prediction.
    """
    # Placeholder behavior until model is added
    if not text or not text.strip():
        return "No text provided"
    return "Coming Soon: Topic model not yet added"
