
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
            "hi": "Hindi",
            "it": "Italian",
            "sp": "Spanish",
            "pt": "Portuguese"
        }
        self.models = {
            "model": AutoModelForSequenceClassification.from_pretrained(self.model_name),
            "tokenizer": AutoTokenizer.from_pretrained(self.model_name),
            "config": AutoConfig.from_pretrained(self.model_name)
        }

    def preprocess(self, text):
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

    def sentiment_single(self, text):
        # Simple preprocessing step
        clean_text = self.preprocess(text)

        # Run tokenizer/model
        encoded_input = self.models["tokenizer"](clean_text, return_tensors = 'pt')
        output = self.models["model"](**encoded_input)

        # Gather scores
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        # Generate output dict
        oupt_dict = {
            self.models["config"].id2label[0]: scores[0],
            self.models["config"].id2label[1]: scores[1],
            self.models["config"].id2label[2]: scores[2],
        }

        # Return to user
        return oupt_dict

    def sentiment_batch(self, text_list):

        # Preprocessing for analysis
        clean_text_list = [self.preprocess(x) for x in text_list]
        oupt_list = []

        # Loop through cleaned text to analyze
        for x in clean_text_list:
            # Run tokenizer/model
            encoded_input = self.models["tokenizer"](x, return_tensors = 'pt')
            cur_output = self.models["model"](**encoded_input)

            # Gather scores
            cur_scores = cur_output[0][0].detach().numpy()
            cur_scores = softmax(cur_scores)
            oupt_dict = {
                self.models["config"].id2label[0]: cur_scores[0],
                self.models["config"].id2label[1]: cur_scores[1],
                self.models["config"].id2label[2]: cur_scores[2],
            }
            oupt_list.append(oupt_dict)
        
        # Return to user
        return oupt_list