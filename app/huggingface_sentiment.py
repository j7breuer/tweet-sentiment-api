

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

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(self.model_name)

    def load_config(self):
        return AutoConfig.from_pretrained(self.model_name)

    def load_model(self):
        return AutoModelForSequenceClassification.from_pretrained(self.model_name)