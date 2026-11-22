
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from threading import Lock


class SentimentAnalyzer:

    _instance = None
    _instance_lock = Lock()
    _model_lock = Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.tokenizer = None
                cls._instance.model = None

        return cls._instance

    def load_model(self):
        with self._model_lock:
            if self.model is None:

                print("Loading FinBERT model...", flush=True)

                tokenizer = AutoTokenizer.from_pretrained(
                    "ProsusAI/finbert"
                )

                model = AutoModelForSequenceClassification.from_pretrained(
                    "ProsusAI/finbert"
                )

                model.eval()

                self.tokenizer = tokenizer
                self.model = model

                print("FinBERT loaded successfully", flush=True)

    def analyze_sentiment(self, text):

        if not text or len(text.strip()) < 10:
            return {
                "label": "neutral",
                "score": 1.0,
                "scores": {
                    "positive": 0.0,
                    "negative": 0.0,
                    "neutral": 1.0
                }
            }

        self.load_model()

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        with torch.inference_mode():
            outputs = self.model(**inputs)

            probabilities = torch.softmax(
                outputs.logits,
                dim=1
            )[0]

        label_idx = probabilities.argmax().item()

        labels = self.model.config.id2label

        return {
            "label": labels[label_idx].lower(),
            "score": probabilities[label_idx].item(),
            "scores": {
                labels[i].lower(): score.item()
                for i, score in enumerate(probabilities)
            }
        }

    def analyze_articles(self, articles):

        for article in articles:

            text = (
                f"{article['title']}. "
                f"{article.get('content') or ''}"
            )

            article["sentiment"] = self.analyze_sentiment(text)

        return articles
