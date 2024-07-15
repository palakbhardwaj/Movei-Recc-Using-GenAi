# RecommendOn - Movie Recommendation System for HackOn

## Features

- Content discovery and personalized Content Advisor leverages ML model powered by Natural Language Processing Model/Large Language Models (LLM), to offer finely tuned content recommendations based on user preferences and location.
- Voice-activated commands, family-friendly filters, curated playlist

## Technology

- React - for frontend
- Node/ExpressJS - for backend
- Fast API to interact with ML model
- Google's Universal Sentence Encoder to generate Vector Embeddings -> [tfhub.dev/google/universal-sentence-encoder/4](https://tfhub.dev/google/universal-sentence-encoder/4)
- Rapid API - to interact with CHAT GPT
- react-speech-recognition - to convert speech from the microphone to text and make it available to your React components
- react-speech - to convert output from Chat-GPT to audio

## Running Locally

### Frontend

```bash
npm install
npm start
```

### Backend
```bash
npm install
npm start
```

### Fast API Model
- To run the Fast API model, follow these steps:

- Install the required Python libraries.
- Run the Fast API application using uvicorn:
```bash
uvicorn model_microservice:app --host 0.0.0.0 --port 8001 --reload
```
This will start the Fast API model microservice, allowing it to interact with your application

