from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API details
api_url = "https://api-inference.huggingface.co/models/gpt2"
headers = {
    "Authorization": "Bearer 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"
}

# Function to query Hugging Face API for text generation
def query_huggingface(prompt):
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    return response.json()

@app.route("/generate", methods=["POST"])
def generate_text():
    # Get the prompt from the request
    data = request.get_json()
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Get the generated response from GPT-2
    result = query_huggingface(prompt)
    
    # Check if the response contains generated text
    if "generated_text" in result[0]:
        return jsonify({"generated_text": result[0]["generated_text"]})
    else:
        return jsonify({"error": "Error generating text"}), 500

if __name__ == "__main__":
    app.run(debug=True)
