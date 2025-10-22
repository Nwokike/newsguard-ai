# 📰 NewsGuard AI

Streamlit app to analyze news articles for credibility, sentiment, clickbait, and more.
🔗 Live App: https://newsguard-ai.streamlit.app/


---

👥 Contributors

Onyeka Nwokike — Team Lead / Topic Classification — https://github.com/Nwokike

Stephen Ayankoso — Fake News Detection — https://github.com/Steve-ayan

Rivaldo — Sentiment Analysis — https://github.com/rivaldo56

Cleiton Langa — Clickbait Detection — https://github.com/cleitonlanga



---

📘 Project Overview

NewsGuard AI is a modular NLP project built with Streamlit.
Each team member contributed a trained model that analyzes different aspects of news articles.
Incomplete modules display as “Coming Soon.”


---

📁 Project Structure

newsguard-ai/
│
├── app.py
│
├── model_functions/
│   ├── topic.py
│   ├── fake.py
│   ├── sentiment.py
│   ├── clickbait.py
│   ├── bias.py              # Coming Soon
│   ├── summarizer.py        # Coming Soon
│   └── emotion.py           # Coming Soon
│
├── models/
│   ├── topic_model.pkl
│   ├── topic_vectorizer.pkl
│   ├── fake_news_model.pkl
│   ├── fake_news_vectorizer.pkl
│   ├── sentiment_model.pkl
│   ├── sentiment_vectorizer.pkl
│   ├── clickbait_model.pkl
│   ├── clickbait_vectorizer.pkl
│   └── ...
│
├── notebooks/
│   ├── topic_classification.ipynb
│   ├── fake_news_training.ipynb
│   ├── sentiment_training.ipynb
│   ├── clickbait_training.ipynb
│   └── ...
│
├── requirements.txt
├── .gitignore
└── README.md


---

🧠 Models

Feature	Function	Status

Topic Classification	predict_topic(text)	✅ Done
Fake News Detection	predict_fake(text)	✅ Done
Sentiment Analysis	predict_sentiment(text)	✅ Done
Clickbait Detection	is_clickbait(text)	✅ Done
Bias Detection	detect_bias(text)	🚧 Coming Soon
Extractive Summarizer	summarize(text)	🚧 Coming Soon
Emotion Detection	get_emotion(text)	🚧 Coming Soon



---

⚙️ Quick Start

git clone https://github.com/Nwokike/newsguard-ai.git
cd newsguard-ai
python -m venv venv
source venv/bin/activate       # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py


---

🧩 Contributing

1. Fork the repo and create a branch:
git checkout -b feature/your-model


2. Add:

Your training notebook → /notebooks

Model + vectorizer → /models

Inference script → /model_functions



3. Push and open a Pull Request to main.




---

📜 License

Apache-2.0
