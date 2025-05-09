#!/bin/bash

set -e
set -o pipefail

pip install -r requirements.txt

echo "STEP 1: Cleaning existed containers..."
cd web
docker-compose down

echo "STEP 2: Constructing and initiating docker services..."
docker-compose up -d --build
cd ..

echo "STEP 3: Waiting MongoDB start..."
sleep 10

echo "STEP 4: Inserting data to MongoDB..."
python tools/upload_mongodb.py
python tools/upload_predict_mongodb.py
echo "Upload finished"

echo "All steps completed!"
echo "App address: http://localhost:8080"
