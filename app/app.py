

import json
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api, fields
from requests.api import request
from restx_models.schemas import api as sentiment_models
from flask_restx.apidoc import apidoc
from huggingface_sentiment import TweetSentimentClassifier
from get_helper import get_help, get_languages, get_single, get_batch
import sys
import os

tsc = TweetSentimentClassifier()
sys.stdout.write(os.getcwd())
# Load help messages
with open("./app/data/metadata/help_metadata.json", encoding = "utf-8") as help_metadata:
    help_metadata_json = json.load(help_metadata)

# Load the API
app = Flask(__name__)
api = Api(app)
api.add_namespace(sentiment_models)

# Define routes
@api.route("/help", methods = ["GET"])
class help(Resource):
    def get(self):
        payload = get_help(help_metadata_json)
        return jsonify(payload)

@api.route("/help/single", methods = ["GET"])
class help_single(Resource):
    def get(self):
        payload = get_single(help_metadata_json)
        return jsonify(payload)

@api.route("/help/batch", methods = ["GET"])
class help_batch(Resource):
    def get(self):
        payload = get_batch(help_metadata_json)
        return jsonify(payload)

@api.route("/help/languages", methods = ["GET"])
class help_languages(Resource):
    def get(self):
        payload = get_languages(help_metadata_json)
        return jsonify(payload)  

@api.route("/sentiment/single", methods = ["POST"])
class sentiment_single(Resource):
    @api.expect(sentiment_models.models['sentiment_single'], validate = True)
    def post(self):
        data = api.payload
        inpt_text = data["text"]
        inpt_lang = data["language"]

        # Check language of text
        if not inpt_lang in tsc.languages_supported.keys():
            abort(400, f"{inpt_lang} not in languages supported by {tsc.model_name}.")

        # Run sentiment model
        oupt = tsc.sentiment_single(inpt_text)

        # Send response
        return jsonify(
            {
                "message": "Successful sentiment analysis of text",
                "data": {
                    "request": {
                        "text": inpt_text,
                        "language": inpt_lang
                    },
                    "response": oupt
                }
            }
        )

'''
@api.route("/sentiment/batch", methods = ["POST"])
class sentiment_batch(Resource):
    @api.expect(sentiment_models.models['sentiment_batch'], validate = True)
    def post(self):
        data = api.payload
        inpt_langs = list(set([x["language"] for x in data]))
        inpt_texts = [x["text"] for x in data]
        
        # Check if all languages of text
        if not all(a in inpt_langs for a in tsc.languages_supported.keys()):
            abort(400, f"Please retry with languages supported by {tsc.model_name}.")

        # Run sentiment model
        oupt = tsc.sentiment_batch(inpt_texts)

        # Send response
        return jsonify(
            {
                "message": "Successful sentiment analysis of text",
                "data": {
                    "request": {
                        "text": ',\n'.join(inpt_texts),
                        "language": ',\n'.join(inpt_langs)
                    },
                    "response": oupt
                }
            }
        )
'''        

if __name__ in "__main__":
    app.run(host = '0.0.0.0', debug  = False)
