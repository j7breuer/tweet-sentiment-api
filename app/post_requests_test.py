
import requests
import json
import sys

# Create body for testing
post_body = {
    "text": "I love you!",
    "language": "en"
}

headers = {'Content-Type': 'application/json'}

# Make request
r = requests.post("http://127.0.0.1:5000/sentiment/single", json = post_body)

# Stdout
sys.stdout.write(f"Status Code: {r.status_code} \nResponse: {json.dumps(r.json(), indent = 4)}\n")