

import json
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api, fields
from requests.api import request
from restx_models.schemas import api as sentiment_models
from flask_restx.apidoc import apidoc
from huggingface_sentiment import TweetSentimentClassifier
import sys

tsc = TweetSentimentClassifier()

# Load the API
app = Flask(__name__)
api = Api(app)
api.add_namespace(sentiment_models)

# Define routes
@api.route("/sentiment/single", methods = ["POST"])
class sentiment_single(Resource):
    @api.expect(sentiment_models.models['sentiment_single'], validate = True)
    def post(self):
        data = api.payload

        # Check language of text
        if not data["language"] in tsc.languages_supported.keys():
            abort(400, f"{data['Language']} not in languages supported by {tsc.model_name}")

        # Run sentiment model
        oupt = tsc.sentiment_single(data['text'])

        return jsonify(
            {
                "message": f"",
                "data": {
                    "request": {
                        "text": data['text'],
                        "language": data['language']
                    },
                    "response": oupt
                }
            }
        )