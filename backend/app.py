from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return {"status": "Math AI Backend Running"}

@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt missing"}), 400

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://najiful85.xyz",
            "X-Title": "Math AI Quiz"
        },
        json={
            "model": "openai/gpt-5.2",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a math teacher. Be clear and concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    result = res.json()

    try:
        answer = result["choices"][0]["message"]["content"]
        return jsonify({"result": answer})
    except:
        return jsonify({"error": result}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
