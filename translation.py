from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face Translation Model (Helsinki-NLP for English to French translation)
TRANSLATION_MODEL = "Helsinki-NLP/opus-mt-en-fr"
HEADERS = {
    "Authorization": "Bearer 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"  
}

def translate_text(text, source_lang="en", target_lang="fr"):
    """
    Translates text using Hugging Face's Helsinki-NLP model.
    Supported languages: en (English), fr (French), de (German), etc.
    Full list: https://huggingface.co/Helsinki-NLP
    """
    payload = {
        "inputs": text,
        "parameters": {
            "src_lang": source_lang,
            "tgt_lang": target_lang
        }
    }
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{TRANSLATION_MODEL}",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Failed to contact Hugging Face API. Status code: {response.status_code}")

    result = response.json()

    # Check if the translation is in the expected format
    if isinstance(result, list) and len(result) > 0 and "translation_text" in result[0]:
        return result[0]["translation_text"]
    elif "error" in result:
        raise Exception(f"Translation error: {result['error']}")
    else:
        raise Exception("Translation failed for an unknown reason.")

@app.route("/translate", methods=["POST"])
def handle_translation():
    data = request.get_json()
    text = data.get("text")
    source_lang = data.get("source_lang", "en")  # Default: English
    target_lang = data.get("target_lang", "fr")  # Default: French

    if not text:
        return jsonify({"error": "Text to translate is required"}), 400

    try:
        result = translate_text(text, source_lang, target_lang)
        return jsonify({"translation": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
