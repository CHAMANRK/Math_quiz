from flask import Flask, request, jsonify, render_template
import requests
import os

# static_folder aur template_folder 'frontend' folder ko point kar rahe hain
app = Flask(__name__, static_folder='frontend', template_folder='frontend')

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    # Sirf text ke bajaye index.html return karein taaki website dikhe
    try:
        return render_template("index.html")
    except:
        return jsonify({"status": "Math AI Backend Running", "note": "index.html not found in frontend folder"})

@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt missing"}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"error": "API Key not configured in Render Environment Variables"}), 500

    res = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://najiful85.xyz",
            "X-Title": "Math AI Quiz"
        },
        json={
            "model": "google/gemini-pro-1.5", # GPT-5.2 abhi available nahi hai, Gemini ya GPT-4 use karein
            "messages": [
                {"role": "system", "content": "You are a math teacher. Be clear and concise."},
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = res.json()

    try:
        answer = result["choices"][0]["message"]["content"]
        return jsonify({"result": answer})
    except Exception as e:
        return jsonify({"error": str(result)}), 500

if __name__ == "__main__":
    # Render ke liye port ko dynamic rakhna zaroori hai
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
