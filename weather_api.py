import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return jsonify({"message": "Weather API is running."})

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' query parameter"}), 400
