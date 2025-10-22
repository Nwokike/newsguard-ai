import pickle
import re
import pathlib
import os

# --- IMPORTANT: Configure Paths to Model Assets ---
# This code uses the relative path to locate the model files in the '../models' directory.
current_dir = pathlib.Path(__file__).parent
MODEL_PATH = current_dir.parent / 'models' / 'fake_news_model.pkl'
VECTORIZER_PATH = current_dir.parent / 'models' / 'fake_news_vectorizer.pkl' 

# --- Text Preprocessing Function (Must match your training steps) ---
def preprocess_text(text: str) -> str:
    """Applies the same cleaning steps used during model training (Phase 2)."""
    # 1. Lowercase
    text = text.lower()
    # 2. Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    # 3. Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

# --- REQUIRED Prediction Function ---
def predict_fake(text: str) -> str:
    """
    Loads the model and vectorizer, predicts fake/real status, 
    and returns a formatted string with the confidence score.
    """
    # Input validation
    if not text or len(text.strip()) < 10:
        return "Not enough text to analyze."
        
    try:
        # Load the model and vectorizer
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
        
        # 1. Preprocess and Vectorize the input text
        cleaned_text = preprocess_text(text)
        vectorized_text = vectorizer.transform([cleaned_text])
        
        # 2. Get Prediction (0 for Fake, 1 for Real) and Probability
        prediction = model.predict(vectorized_text)[0] 
        probability_score = model.predict_proba(vectorized_text)[0][prediction] * 100
        
        # 3. Format the Output string as requested: "Risk (Label) - XX.XX%"
        label = "Real News" if prediction == 1 else "Fake News"
        risk_level = "Low Risk" if prediction == 1 else "High Risk"
        
        return f"{risk_level} ({label}) - {probability_score:.2f}%"

    except FileNotFoundError:
        # This error is critical and tells the Team Lead the model files are missing
        return "Error: Model assets not found. Check /models folder paths."
    except Exception as e:
        # Catch any other runtime error during prediction
        return f"Error running model: Failed to predict. ({type(e).__name__})"

# --- Optional Test Block (Runs only if you execute fake.py directly) ---
if __name__ == '__main__':
    print("--- Local Test Run ---")
    test_text_fake = "Aliens stole all the world's coffee beans today."
    print(f"Test 1 (Fake): {predict_fake(test_text_fake)}") 
    
    test_text_real = "The local government council announced a new public transit schedule effective next month."
    print(f"Test 2 (Real): {predict_fake(test_text_real)}")
