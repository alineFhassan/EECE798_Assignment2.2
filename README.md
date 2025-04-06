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
   python file_name.py
 
## Sentiment Analysis API  

A RESTful API for sentiment analysis using a pre-trained Hugging Face Transformers model.  

### Features  
- Analyzes text sentiment (Positive, Negative, Neutral)  
- Fast inference with a pre-trained NLP model  
- Simple HTTP endpoint for easy integration  

### Postman 

1. **Example Responses  for Sentiment Analysis API**
- **Positive Sentiment**:  
  ```json  
  {  
      "text": "I love this amazing API! It's fantastic!",  
      "sentiment": "Positive"  
  }  
  ```  

- **Negative Sentiment**:  
  ```json  
  {  
      "text": "This is terrible and I hate it!",  
      "sentiment": "Negative"  
  }  
  ```  

- **Neutral Sentiment**:  
  ```json  
  {  
      "text": "The weather is cloudy today.",  
      "sentiment": "Neutral"  
  }  
  ```  

- **Testing with Postman** 
1. Open Postman and set the request to `POST`.  
2. Enter the URL: `http://localhost:8000/analyze`.  
3. Set the body to `raw` > `JSON` and input your text.  

