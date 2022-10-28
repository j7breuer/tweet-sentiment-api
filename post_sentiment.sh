#!/bin/bash
curl -i -H "Content-Type: application/json" -X POST -d "{\"language\": \"en\", \"text\": \"hello\"}" http://192.168.50.21:5000/sentiment/single