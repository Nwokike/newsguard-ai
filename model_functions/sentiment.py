import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os

# --- NLTK Setup ---
# This ensures stopwords are available
try:
    stopwords_list = set(stopwords.words('english'))
except LookupError:
    print("NLTK stopwords not found. Downloading...")
    nltk.download('stopwords')
    stopwords_list = set(stopwords.words('english'))
    
ps = PorterStemmer()

# --- File Paths ---
# This assumes the script is in 'model_functions'
# and the models are in 'models' at the same root level.
try:
    # Gets the directory of this script (model_functions)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Fallback for environments where __file__ isn't defined
    SCRIPT_DIR = os.path.abspath(os.path.join(os.getcwd(), 'model_functions'))

# Go up one level to the project root
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')

# --- Load Models ---
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    models_loaded = True
    print("Sentiment models loaded successfully.")
except FileNotFoundError:
    print(f"Warning: Model files not found. Searched in {MODELS_DIR}")
    model = None
    vectorizer = None
    models_loaded = False
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None
    models_loaded = False


# --- (FIX 1) Correct Preprocessing Function ---
# This function is now IDENTICAL to the one from the training notebook.

def preprocess_text(text):
    """Cleans and preprocesses raw text."""
    text = str(text) # Ensure it's a string
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove non-alphabetic characters
    text = text.lower() # Convert to lowercase
    text = text.split() # Tokenize
    text = [word for word in text if word not in stopwords_list] # Remove stopwords
    text = [ps.stem(word) for word in text] # Stemming
    return ' '.join(text)

# --- (FIX 2) Correct Prediction Function ---

def predict_sentiment(text):
    """
    Predicts the sentiment of a given text.
    Returns 'Positive', 'Negative', 'Neutral', or an error message.
    """
    if not models_loaded or model is None or vectorizer is None:
        return "Sentiment Model Not Loaded"

    try:
        # 1. Preprocess the input text using the correct function
        cleaned_text = preprocess_text(text)

        # 2. Transform the text using the loaded vectorizer
        text_vector = vectorizer.transform([cleaned_text])

        # 3. Make a prediction
        prediction = model.predict(text_vector)

        # 4. THE FIX: The model already returns the string (e.g., 'neutral')
        # No dictionary map is needed.
        sentiment = prediction[0]

        return sentiment

    except Exception as e:
        print(f"Error during sentiment prediction: {e}")
        return "Error in Prediction"

# --- Main block for testing ---
if __name__ == "__main__":
    # This block runs only when you execute this script directly
    # (e.g., `python model_functions/sentiment.py`)

    if models_loaded:
        print("\n--- Testing Sentiment Model ---")

        test_text_pos = "The company's profits increased significantly last quarter."
        test_text_neg = "The new product launch was a complete failure, shares dropped."
        test_text_neu = "The stock market remained stable today."

        print(f"Text: \"{test_text_pos}\"")
        print(f"Prediction: {predict_sentiment(test_text_pos)}") # Should be positive/neutral

        print(f"\nText: \"{test_text_neg}\"")
        print(f"Prediction: {predict_sentiment(test_text_neg)}") # Should be negative

        print(f"\nText: \"{test_text_neu}\"")
        print(f"Prediction: {predict_sentiment(test_text_neu)}") # Should be neutral
    else:
        print("\n--- Testing Halted ---")
        print("Models could not be loaded. Check file paths.")
