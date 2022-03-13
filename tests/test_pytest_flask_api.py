
import json

def test_sentiment_single(client, expected_sentiment_single):
    app = client
    req_resp = expected_sentiment_single
    expected_response = req_resp['response']
    expected_request = req_resp['request']
    response = app.post("/sentiment/single", json = expected_request)
    response_json = response.json
    assert response.status_code == 200
    assert response_json == expected_response

def test_fail_language_sentiment_single(client, fail_language_sentiment_single):
    app = client
    req_resp = fail_language_sentiment_single
    expected_response = req_resp['response']
    expected_request = req_resp['request']
    response = app.post("/sentiment/single", json = expected_request)
    response_json = response.json
    assert response.status_code == 500
    assert response_json == "sample"