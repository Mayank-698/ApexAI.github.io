from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your OpenAI API key
OPENAI_API_KEY = "your_openai_api_key_here"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    # OpenAI GPT (Free Tier)
    openai_response = get_openai_response(question)

    # HuggingFace Free Model (OpenAssistant)
    hf_response = get_huggingface_response(question)

    return render_template(
        "index.html",
        question=question,
        openai_response=openai_response,
        hf_response=hf_response
    )

def get_openai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"OpenAI Error: {e}"

def get_huggingface_response(prompt):
    try:
        headers = {"Authorization": "Bearer hf_YOUR_HF_API_KEY"}
        json_data = {"inputs": prompt}
        response = requests.post(
            "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
            headers=headers,
            json=json_data
        )
        return response.json()[0]["generated_text"].strip()
    except Exception as e:
        return f"HuggingFace Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
