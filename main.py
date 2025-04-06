from flask import Flask, request, jsonify
import requests
from typing import Optional

app = Flask(__name__)

# Configuration for all Hugging Face services
HF_CONFIG = {
    "api_key": "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",  
    "models": {
        "text_generation": "gpt2",
        "summarization": "facebook/bart-large-cnn",
        "translation": "Helsinki-NLP/opus-mt-en-fr",
        "keyphrase_extraction": "ml6team/keyphrase-extraction-kbir-inspec",
        "sentiment_analysis": "cardiffnlp/twitter-roberta-base-sentiment"
    }
}

HEADERS = {"Authorization": f"Bearer {HF_CONFIG['api_key']}"}

def query_huggingface(model_name: str, payload: dict) -> dict:
    """Generic function to query any Hugging Face model"""
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_name}",
        headers=HEADERS,
        json=payload
    )
    
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")
    
    return response.json()

# Text Generation Endpoint
@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.get_json()
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        result = query_huggingface(
            HF_CONFIG["models"]["text_generation"],
            {"inputs": prompt}
        )
        
        if isinstance(result, list) and "generated_text" in result[0]:
            return jsonify({"generated_text": result[0]["generated_text"]})
        return jsonify({"error": "Generation failed", "details": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Summarization Endpoint
@app.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text is required"}), 400

    params = {
        "max_length": data.get("max_length", 130),
        "min_length": data.get("min_length", 30),
        "do_sample": False
    }

    try:
        result = query_huggingface(
            HF_CONFIG["models"]["summarization"],
            {"inputs": text, "parameters": params}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return jsonify({"summary": result[0]["summary_text"]})
        elif "summary_text" in result:
            return jsonify({"summary": result["summary_text"]})
        return jsonify({"error": "Summarization failed", "details": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Translation Endpoint
@app.route("/translate", methods=["POST"])
def translate_text():
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text is required"}), 400

    params = {
        "src_lang": data.get("source_lang", "en"),
        "tgt_lang": data.get("target_lang", "fr")
    }

    try:
        result = query_huggingface(
            HF_CONFIG["models"]["translation"],
            {"inputs": text, "parameters": params}
        )
        
        if isinstance(result, list) and len(result) > 0:
            return jsonify({"translation": result[0]["translation_text"]})
        return jsonify({"error": "Translation failed", "details": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keyphrase Extraction Endpoint
@app.route("/extract", methods=["POST"])
def extract_keyphrases():
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        result = query_huggingface(
            HF_CONFIG["models"]["keyphrase_extraction"],
            {"inputs": text}
        )
        
        if isinstance(result, list):
            # Filter and sort keyphrases
            min_confidence = float(data.get("min_confidence", 0.5))
            top_n = int(data.get("top_n", 10))
            
            filtered = [
                (kp["word"], kp["score"])
                for kp in result
                if "word" in kp and "score" in kp and kp["score"] >= min_confidence
            ]
            filtered.sort(key=lambda x: x[1], reverse=True)
            
            if top_n > 0:
                filtered = filtered[:top_n]
            
            keyphrases, scores = zip(*filtered) if filtered else ([], [])
            
            return jsonify({
                "keyphrases": list(keyphrases),
                "scores": list(scores),
                "count": len(keyphrases)
            })
        return jsonify({"error": "Extraction failed", "details": result}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    data = request.get_json()
    text = data.get("text")
    
    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        result = query_huggingface(
            HF_CONFIG["models"]["sentiment_analysis"],
            {"inputs": text}
        )

        print("Hugging Face result:", result)

        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
            predictions = result[0]
            # Get the label with the highest score
            top_prediction = max(predictions, key=lambda x: x["score"])
            
            label_map = {
                "LABEL_0": "NEGATIVE",
                "LABEL_1": "NEUTRAL",
                "LABEL_2": "POSITIVE"
            }

            return jsonify({
                "sentiment": label_map.get(top_prediction["label"], top_prediction["label"]),
                "confidence": top_prediction["score"]
            })

        return jsonify({"error": "Unexpected response format", "details": result}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)