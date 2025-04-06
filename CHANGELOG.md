# Changelog
All notable changes to this assignment will be documented in this file.

## [1.0.0]
### Added
- Can be used for Text generation
- Can be used for any purpose that is supported by GPT2
- Created a `/generate` endpoint

## [2.0.0]
### Added
- Produces concise summaries (default: 30-130 words).
- Customizable Length
- Created a `/summarize` endpoint

## [3.0.0]
### Added
- Translates text from a source language (default: English "en") to a target language (default: French "fr").
- Uses the Helsinki-NLP/opus-mt-en-fr model, specialized for English→French translation.
- Created a `/translate` endpoint

## [4.0.0]
### Added
- Analyzes text sentiment (Positive, Negative, Neutral)  
- Fast inference with a pre-trained NLP model  
- Created a `/analyze` endpoint

## [5.0.0]
### Added
- Accept a block of text and return important keyphrases from it.
- Model used: ml6team/keyphrase-extraction-kbir-inspec
- Created a `/extract` endpoint

## [6.0.0]
### Released
- Include all the created endpoints
