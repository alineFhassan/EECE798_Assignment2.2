from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Initialize FastAPI app
app = FastAPI(
    title="Sentiment Analysis API",
    description="A simple API for sentiment analysis using Hugging Face Transformers",
    version="1.0.0"
)

API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
# Hugging Face API configuration
HEADERS = {
    "Authorization": "Bearer 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"
}

class TextInput(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    label: str  # Adding label to show the raw model output

@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API"}

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(text_input: TextInput):
    try:
        # Make request to Hugging Face Inference API
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": text_input.text}
        )
        
        # Check for errors
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Hugging Face API error: {response.text}"
            )
        
        # Get the results (structure might be different)
        results = response.json()
        
        # Handle cases where the model is still loading
        if isinstance(results, dict) and 'error' in results:
            raise HTTPException(
                status_code=503,
                detail=f"Model is loading: {results['error']}"
            )
        
        # Find the highest confidence result
        if isinstance(results, list) and len(results) > 0:
            # For this model, the output is a list of dictionaries for each label
            best_result = max(results[0], key=lambda x: x['score'])
        else:
            raise HTTPException(
                status_code=500,
                detail="Unexpected response format from Hugging Face API"
            )

        # Map the model's output to our response
        sentiment_mapping = {
            'LABEL_0': 'NEGATIVE',
            'LABEL_1': 'NEUTRAL',
            'LABEL_2': 'POSITIVE'
        }
        
        return SentimentResponse(
            sentiment=sentiment_mapping[best_result['label']],
            confidence=best_result['score'],
            label=best_result['label']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)