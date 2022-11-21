#!/bin/bash
help_endpoints=(
    http://127.0.0.1:5000/help
    http://127.0.0.1:5000/help/single
    http://127.0.0.1:5000/help/batch
    http://127.0.0.1:5000/help/languages
)

for url in "${help_endpoints}[@]"; do
    curl "$url"
done
