
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
        '''
        desc:
            Given an input text in the form of a tweet, return the tweet cleaned
        inpt:
            text [str]: tweet to be cleaned
        oupt:
            [text]: text with usernames and urls removed
        '''
        new_text = []
        for t in text.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t # Replace this with a better regex pattern...
            t = 'http' if t.startswith('http') else t # Replace this with a better regex pattern...
            new_text.append(t)
        return " ".join(new_text)

    def sentiment_single(self, text):
        '''
        desc:
            Given an input text in the form of a cleaned tweet, analyze the text
            for sentiment scores - positive/neutral/negative
        inpt: 
            text [str]: cleaned tweet
        oupt:
            oupt_dict [dict]: key/value pairs of negative, neutral, and positive scores
        '''
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
            self.models["config"].id2label[0]: float('%.5f' % scores[0]),
            self.models["config"].id2label[1]: float('%.5f' % scores[1]),
            self.models["config"].id2label[2]: float('%.5f' % scores[2])
        }

        # Return to user
        return oupt_dict

    def sentiment_batch(self, text_list):
        '''
        desc:
            Given an input text in the form of a cleaned tweet, analyze the text
            for sentiment scores - positive/neutral/negative
        inpt: 
            text_list [list]: list of cleaned tweets
        oupt:
            oupt_list [list]: list of dicts with key/value pairs of negative, neutral, and positive scores
        '''
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
                self.models["config"].id2label[0]: float('%.5f' % cur_scores[0]),
                self.models["config"].id2label[1]: float('%.5f' % cur_scores[1]),
                self.models["config"].id2label[2]: float('%.5f' % cur_scores[2])
            }
            oupt_list.append(oupt_dict)
        
        # Return to user
        return oupt_list