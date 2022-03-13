
import pytest
import sys

sys.path.append("../app")

from app import app as root_app

@pytest.fixture(scope = "session")
def client():
    root_app.testing = True
    with root_app.test_client() as client:
        yield client
    
@pytest.fixture()
def expected_sentiment_single():
    oupt = {}
    oupt['response'] = {
        "data": {
            "request": {
                "language": "en",
                "text": "YESSSSSSSSS!!!!!!!!!!! A BRAVE HEADER FROM LUIS DIAZ!!!!!!!!!!!"
            },
            "response": {
                "Negative": 0.02395,
                "Neutral": 0.078,
                "Positive": 0.89806
            }
        },
        "message": "Successful sentiment analysis of text"
    }
    oupt['request'] = {
        "text": "YESSSSSSSSS!!!!!!!!!!! A BRAVE HEADER FROM LUIS DIAZ!!!!!!!!!!!",
        "language": "en"
    }
    return oupt

@pytest.fixture()
def fail_language_sentiment_single():
    oupt = {}
    oupt['request'] = {
        "text": "YESSSSSSSSS!!!!!!!!!!! A BRAVE HEADER FROM LUIS DIAZ!!!!!!!!!!!",
        "language": "abcd"
    }
    oupt['response'] = {
        "message": "abcd not in languages supported by cardiffnlp/twitter-xlm-roberta-base-sentiment."
    }
    return oupt