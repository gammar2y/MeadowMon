# filepath: /c:/Users/acrew/OneDrive/Desktop/MeadowMon/server/djangoproj/app.py
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

app = Flask(__name__)
backend_url = os.getenv('MONGODB_URI')
print(f"Backend URL: {backend_url}")

client = MongoClient(backend_url)
db = client['MeadowMon']

@app.route('/')
def index():
    collection = db['your-collection']
    data = list(collection.find({}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=3000)