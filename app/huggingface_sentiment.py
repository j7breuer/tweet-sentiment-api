
from collections import defaultdict
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax

class TweetSentimentClassifier:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        self.languages_supported = {
            "en": "English",
            "ar": "Arabic",
            "fr": "French",
            "de": "German",
            "hi": "hindi",
            "it": "italian",
            "sp": "spanish",
            "pt": "portuguese"
        }
        self.models = {
            "model": AutoModelForSequenceClassification.from_pretrained(self.model_name),
            "tokenizer": AutoTokenizer.from_pretrained(self.model_name),
            "config": AutoConfig.from_pretrained(self.model_name)
        }

    def preprocess(text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def sentiment_single(self, text):
        # Simple preprocessing step
        text = self.preprocess(text)

        # Run tokenizer/model
        encoded_input = self.tokenizer(text, return_tensors = 'pt')
        output = self.model(**encoded_input)

        # Gather scores
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        # Generate output dict
        oupt_dict = {
            self.config.id2label[0]: scores[0],
            self.config.id2label[1]: scores[1],
            self.config.id2label[2]: scores[2]
        }