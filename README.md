
# Tweet Sentiment Microservice [Beta]
Flask API that provides tweet sentiment using the twitter-XLM-roBERTa-base model that is integrated into the <a href="https://github.com/cardiffnlp/tweetnlp">TweetNLP library</a>.  The HuggingFace page for the model used by the API can be found <a href="https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment">here</a>. 

Supported languages:
- English: en
- Arabic: ar
- French: fr
- German: de
- Hindi: hi
- Italian: it
- Spanish: sp
- Portuguese: pt

## Installation
By default, the tweet sentiment model will run off of CPU.  If you'd like to run off of GPU to speed up inference time, please configure torch to point to your GPU.

### Install requirements.txt first
```
pip install -r requirements.txt
```

### You may need to install sentencepiece an alternative way
```
pip install transformers[sentencepiece]
```

### Install PyTorch and CUDA accordingly
You can do this by defaulting to the specifications of requirements.txt or by going to the following website and using the onscreen prompt: https://pytorch.org/get-started/locally/

## Usage
Expect response to follow this format:

```json
{
  "data": {
    "request":{
      "language":"en",
      "text":"I love developing Flask APIs"
    },
    "response":{
      "negative":0.01437,
      "neutral":0.09704,
      "positive":0.8886
    }
  },
  "message":"Successful sentiment analysis of text"
}
```

## Endpoints:

### GET API Help

'GET /help'

**Response**

- '200 OK' on success

```json
{
  "This is an API meant to conduct basic sentiment classification between 8 languages using various transformer based tweet sentiment models."
}
```

### GET API Help Single

'GET /help/single'

**Response**

- '200 OK' on success

```json
{
  "request_example":{
    "language":"en",
    "text":"I love creating Python Flask APIs"
  },
  "response_example":{
    "data":{
      "request":{
        "language":"en",
        "text":"I love creating Python Flask APIs"
      },
      "response":{
        "Negative":0.01408,
        "Neutral":0.09497,
        "Positive":0.89095
      }
    },
    "message":"Successful sentiment analysis of text"
  }
}
```

### GET API Help Batch

'GET /help/batch'

**Response**

- '200 OK' on success

```json
{
  "request_example":{
    "language":"en", 
    "text":"I love creating Python Flask APIs"
  },
  "response_example":{
    "data":{
      "request":{
        "language":"en",
        "text":"I love creating Python Flask APIs"
      },
      "response":{
        "Negative":0.01408,
        "Neutral":0.09497,
        "Positive":0.89095
      }
    },
    "message":"Successful sentiment analysis of text"
  }
}
```

### POST Tweet Sentiment Single

'POST /sentiment/single'

**Request**
```json
{
  "text": "I love developing Flask APIs",
  "language": "en"
}
```

**Response**
- '200 OK' on success

```json
{
  "data": {
    "request":{
      "language":"en",
      "text":"I love developing Flask APIs"
    },
    "response":{
      "negative":0.01437,
      "neutral":0.09704,
      "positive":0.8886
    }
  },
  "message":"Successful sentiment analysis of text"
}
```

