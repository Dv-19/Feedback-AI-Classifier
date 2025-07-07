# classifier.py
import torch
from transformers import pipeline
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FeedbackClassifier:
    def __init__(self):
        """Initializes the classifier and loads the necessary models."""
        self.categories = ['Academics', 'Facilities', 'Administration']
        self.category_classifier = None
        self.sentiment_analyzer = None

        try:
            logging.info("Initializing models... This may take a few minutes on first run.")
            self.category_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU
            )
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1  # Use CPU
            )
            logging.info("✅ All models loaded successfully.")

        except Exception as e:
            logging.error(f"💥 Failed to load one or more models: {e}", exc_info=True)

    def classify(self, text):
        """Classifies feedback for both category and sentiment."""
        if not self.category_classifier or not self.sentiment_analyzer:
            raise RuntimeError("Classifier models are not available. Check server logs.")

        if not text or not isinstance(text, str) or not text.strip():
            return {
                'category': 'Unknown', 'category_confidence': 0.0,
                'sentiment': 'Unknown', 'sentiment_confidence': 0.0
            }

        # Get Category
        category_prediction = self.category_classifier(text, self.categories)
        category_result = {
            'category': category_prediction['labels'][0],
            'category_confidence': round(category_prediction['scores'][0], 2)
        }

        # Get Sentiment
        sentiment_prediction = self.sentiment_analyzer(text)[0]
        sentiment_result = {
            'sentiment': sentiment_prediction['label'].capitalize(),
            'sentiment_confidence': round(sentiment_prediction['score'], 2)
        }

        # Combine results
        return {**category_result, **sentiment_result}

    def classify_batch(self, texts):
        """Classifies a batch of feedback texts."""
        if not self.category_classifier or not self.sentiment_analyzer:
            raise RuntimeError("Classifier models are not available.")
        
        return [self.classify(text) for text in texts if text and text.strip()]