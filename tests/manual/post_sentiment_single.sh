#!/bin/bash
curl -i -H "Content-Type: application/json" -X POST -d "{\"language\": \"en\", \"text\": \"I love creating Python Flask APIs\"}" http://192.168.50.21:5000/sentiment/single