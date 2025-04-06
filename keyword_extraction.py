from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

# Initialize FastAPI app
app = FastAPI(
    title="Keyphrase Extraction API",
    description="A simple API for extracting keyphrases from text using Hugging Face Transformers",
    version="1.0.0"
)

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/ml6team/keyphrase-extraction-kbir-inspec"
HEADERS = {
    "Authorization": "Bearer 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"
}

class TextInput(BaseModel):
    text: str
    min_confidence: float = 0.5  # Optional threshold for confidence filtering
    top_n: int = 10  # Optional limit on number of keyphrases to return

class KeyphraseResponse(BaseModel):
    keyphrases: list[str]
    scores: list[float]
    count: int

def query_huggingface(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

@app.get("/")
async def root():
    return {"message": "Welcome to the Keyphrase Extraction API"}

@app.post("/extract", response_model=KeyphraseResponse)
async def extract_keyphrases(text_input: TextInput):
    try:
        # Get keyphrase extraction results from Hugging Face API
        payload = {"inputs": text_input.text}
        results = query_huggingface(payload)
        
        if isinstance(results, dict) and 'error' in results:
            raise HTTPException(status_code=500, detail=results['error'])
        
        # Process results (assuming they come in the same format as the local model)
        filtered_results = [
            (result['word'], result['score']) 
            for result in results 
            if result['score'] >= text_input.min_confidence
        ]
        
        # Sort by confidence score (descending)
        filtered_results.sort(key=lambda x: x[1], reverse=True)
        
        # Apply top_n limit
        if text_input.top_n > 0:
            filtered_results = filtered_results[:text_input.top_n]
        
        # Separate phrases and scores for response
        phrases, scores = zip(*filtered_results) if filtered_results else ([], [])
        
        return KeyphraseResponse(
            keyphrases=list(phrases),
            scores=list(scores),
            count=len(phrases)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)