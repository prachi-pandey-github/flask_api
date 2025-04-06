from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if available

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # or replace with your key as a string

def get_gemini_response(prompt):
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-001:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, params=params, json=data)

    if response.status_code == 200:
        reply = response.json()
        try:
            return reply["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "No valid response received from Gemini."
    else:
        return f"Error: {response.status_code} - {response.text}"



app = Flask(__name__)
load_dotenv()

@app.route("/get-recommendation", methods=["GET"])
def get_recommendation():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Please provide a query parameter"}), 400

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-thinking-exp-01-21:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [{"parts": [{"text": query}]}]
    }

    response = requests.post(url, headers=headers, params=params, json=data)

    if response.status_code == 200:
        result = response.json()
        try:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"response": text})
        except Exception as e:
            return jsonify({"error": "Failed to parse Gemini response", "details": str(e)})
    else:
        return jsonify({"error": "Gemini API error", "details": response.text}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

