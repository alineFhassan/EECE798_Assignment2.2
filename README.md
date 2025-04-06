# EECE798_Assignment2.2

## Team Members  
- Aline Hassan  
- Zainab Saad  


## Setup  
1. **Create Conda Environment**:  
   ```bash  
   conda env create -f environment.yml  
   conda activate github  
   ```  

2. **Run the API**:  
   cd /path/to/your/project/folder  
   python main.py
 
## Sentiment Analysis API  

A RESTful API for sentiment analysis using a pre-trained Hugging Face Transformers model.  
 
- **Testing with Postman** 
1. Open Postman and set the request to `POST`.  
2. Enter the URL: `http://localhost:5000/analyze`.  
3. Set the body to `raw` > `JSON` and input your text.
   
### Features  
- Analyzes text sentiment (Positive, Negative, Neutral)  
- Fast inference with a pre-trained NLP model  
- Simple HTTP endpoint for easy integration
 
## Text Summarization API
A Restful API for summarizing text using a pre-trained Hugging Face Transformers model. 

### Features 
- Produces concise summaries (default: 30-130 words).
- Customizable Length
- Optional max_length and min_length parameters to control summary size.
  
- **Testing with Postman** 
1. Open Postman and set the request to `POST`.  
2. Enter the URL: `http://localhost:5000/summarize`.  
3. Set the body to `raw` > `JSON` and input your text.

## Translation
A Restful API for translating texts

### Features
- Translates text from a source language (default: English "en") to a target language (default: French "fr").
- Uses the Helsinki-NLP/opus-mt-en-fr model, specialized for English→French translation.

- **Testing with Postman** 
1. Open Postman and set the request to `POST`.  
2. Enter the URL: `http://localhost:5000/translate`.  
3. Set the body to `raw` > `JSON` and input your text.

## General Purpose API
A Restful API for text generation using a pre-trained Hugging Face Transformers model (GPT2). 

### Features
- Can be used for Text generation
- Can be used for any purpose that is supported by GPT2

- **Testing with Postman** 
1. Open Postman and set the request to `POST`.  
2. Enter the URL: `http://localhost:5000/generate`.  
3. Set the body to `raw` > `JSON` and input your text.

## Keyword Extraction
A Restful API for keyword extraction using a pre-trained Hugging Face Transformers model 

### Features
- Accept a block of text and return important keyphrases from it.
- Model used: ml6team/keyphrase-extraction-kbir-inspec

- **Testing with Postman** 
1. Open Postman and set the request to `POST`.  
2. Enter the URL: `http://localhost:5000/extract`.  
3. Set the body to `raw` > `JSON` and input your text.
