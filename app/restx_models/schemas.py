
from flask_restx import fields, Namespace

api = Namespace("Tweet Sentiment Models", description = "namespace for tweet sentiment API models")

#========================#
# Tweet Sentiment Single #
#========================#

sentiment_single_schema = {
    "text": fields.String(description = "Text to be analyzed by API", required = True)
}

sentiment_single_model = api.model("sentiment_single", sentiment_single_schema)

#=======================#
# Tweet Sentiment Batch #
#=======================#

sentiment_batch_schema = {
    "text": fields.List(fields.Nested(api.model("sentiment_single", sentiment_single_schema)), required = True)
}

sentiment_batch_model = api.model("sentiment_batch", sentiment_batch_schema)