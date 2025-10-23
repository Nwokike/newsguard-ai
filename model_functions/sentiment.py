import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os

# --- Configuration ---

# Get the directory of the current script
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Define file paths relative to the script's directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')

# --- Load Models ---

# Load the trained model and vectorizer
# We use a try-except block to handle missing files gracefully in the Streamlit app
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    models_loaded = True
    print("Sentiment models loaded successfully.")
except FileNotFoundError:
    print(f"Warning: Model or vectorizer file not found. {MODEL_PATH} or {VECTORIZER_PATH}")
    model = None
    vectorizer = None
    models_loaded = False
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None
    models_loaded = False


# --- Preprocessing Function ---

# This MUST be the same function used during training
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

stemmer = PorterStemmer()

def preprocess_text(text):
    """Cleans and preprocesses raw text."""
    # 1. Lowercase
    text = str(text).lower()
    # 2. Remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', '', text)
    # 3. Remove stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    # 4. Stemming
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text

# --- Prediction Function ---

def predict_sentiment(text):
    """
    Predicts the sentiment of a given text.
    Returns 'Positive', 'Negative', 'Neutral', or an error message.
    """
    if not models_loaded or model is None or vectorizer is None:
        # This allows the Streamlit app to still run and show "Coming Soon"
        # or a similar message if the model files are missing.
        return "Sentiment Model Not Loaded"

    try:
        # 1. Define the reverse label map
        # (Must match the one used in the notebook)
        reverse_label_map = {0: 'Neutral', 1: 'Positive', 2: 'Negative'}

        # 2. Preprocess the input text
        cleaned_text = preprocess_text(text)

        # 3. Transform the text using the loaded vectorizer
        text_vector = vectorizer.transform([cleaned_text])

        # 4. Make a prediction
        prediction = model.predict(text_vector)

        # 5. Map the numerical prediction back to a string label
        sentiment = reverse_label_map.get(prediction[0], "Unknown")

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
        print(f"Prediction: {predict_sentiment(test_text_pos)}")

        print(f"\nText: \"{test_text_neg}\"")
        print(f"Prediction: {predict_sentiment(test_text_neg)}")

        print(f"\nText: \"{test_text_neu}\"")
        print(f"Prediction: {predict_sentiment(test_text_neu)}")
    else:
        print("\n--- Testing Halted ---")
        print("Models could not be loaded. Place .pkl files in the same directory.")