from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face API details for a summarization model
api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {
    "Authorization": "Bearer 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"
}

# Function to query Hugging Face API for text summarization
def query_huggingface(text_to_summarize, max_length=130, min_length=30):
    payload = {
        "inputs": text_to_summarize,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False  # For more deterministic results
        }
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

@app.route("/summarize", methods=["POST"])
def summarize_text():
    # Get the text to summarize from the request
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text to summarize is required"}), 400

    max_length = data.get("max_length", 130)
    min_length = data.get("min_length", 30)

    # Get the summary
    try:
        result = query_huggingface(text, max_length, min_length)
        
        # Check if the response contains the summary
        if isinstance(result, list) and len(result) > 0:
            return jsonify({"summary": result[0]["summary_text"]})
        elif "summary_text" in result:
            return jsonify({"summary": result["summary_text"]})
        else:
            return jsonify({"error": "Error generating summary", "details": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)