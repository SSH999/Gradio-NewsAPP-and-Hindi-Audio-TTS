---
title: News Sentiment Analysis App
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.19.1"
app_file: app.py
pinned: false
---

# News Summarization and Sentiment Analysis App

This comprehensive application extracts news articles, performs sentiment analysis, identifies key topics, and generates Hindi audio summaries. It features both a Gradio interface for easy interaction and a FastAPI endpoint for API access.

---

## Deploying on Hugging Face Spaces

### Step 1: Create a Hugging Face Space
1. Visit [Hugging Face Spaces](https://huggingface.co/spaces).
2. Click **Create New Space**.
3. Set the **SDK** to **Gradio**.
4. Upload the following files:
   - `app.py` (Main application logic)
   - `requirements.txt` (Dependencies)
   - `README.md` (This guide)

### Step 2: Launch the Application
1. After uploading the files, click **Deploy**.
2. Hugging Face will automatically build and launch your application.
3. Once deployment is complete, a **public URL** will be available for both the Gradio interface and FastAPI endpoint.

---

## Key Features
**News Extraction:** Retrieves news articles via NewsAPI for a specified company.  
**Sentiment Analysis:** Classifies content as Positive, Negative, or Neutral.  
**Comparative Analysis:** Provides insights on sentiment distribution and coverage differences.  
**Hindi Text-to-Speech (TTS):** Generates an audio summary in Hindi.  
**FastAPI Endpoint:** Enables API integration for programmatic access.  
**Gradio Interface:** Simplifies user interaction with an intuitive web-based UI.  
**Ngrok Integration:** Enables public URL generation in Colab environments.  

---

## How the Application Works

### 1 News Extraction
- The application connects to NewsAPI to fetch articles based on the given company name.
- Up to **10 articles** are retrieved for analysis.
- Each article includes the **title**, **summary**, and **full content** (if available).

### 2 Topic Extraction
- Key topics are identified using the **KeyBERT** library for deeper insights into article content.
- The application compares unique and common topics across extracted articles.

### 3 Sentiment Analysis
- Each article’s content undergoes sentiment analysis using the **transformers pipeline**.
- Sentiments are classified as **Positive**, **Negative**, or **Neutral**.

### 4 Comparative Analysis
- The app calculates:
  - Total count of Positive, Negative, and Neutral articles.
  - Highlights key differences between Positive and Negative coverage.

### 5 Audio Summary (Hindi TTS)
- The summarized insights are translated into Hindi and converted to speech using **gTTS**.
- The result is saved as an **MP3 file** for easy listening.

### 6 FastAPI Endpoint
- The FastAPI endpoint allows automated data retrieval using:
```
https://your-space-url.hf.space/analyze?company_name=Tesla
```
- The response includes:
  - Extracted articles with sentiment labels
  - Comparative analysis results
  - Downloadable Hindi audio file

### 7 Gradio Interface
- The Gradio UI allows users to:
  - Enter a company name
  - View article details, sentiment results, and insights
  - Download the Hindi audio summary

---

## Using the Gradio Interface
1. Open the Gradio link displayed after deployment.
2. Enter the **company name** in the text field (e.g., `Tesla`).
3. Click **Submit** to generate:
   - Extracted articles with sentiment labels.  
   - Comparative sentiment summary.  
   - Downloadable Hindi audio summary.  

---

## Accessing the FastAPI Endpoint
1. Copy the FastAPI URL displayed during deployment (e.g., `https://your-space-url.hf.space`).
2. Use the following pattern for API requests:
```
https://your-space-url.hf.space/analyze?company_name=Tesla
```
3. Example JSON Output:
```json
{
    "Company": "Tesla",
    "Articles": [
        { "title": "Tesla hits record sales", "sentiment": "POSITIVE" },
        { "title": "Stock prices fall", "sentiment": "NEGATIVE" }
    ],
    "Comparative Sentiment Score": {
        "Sentiment Distribution": { "Positive": 5, "Negative": 3, "Neutral": 2 },
        "Coverage Differences": [
            {"Comparison": "Positive articles highlight achievements", "Impact": "Mixed reviews may affect investors"}
        ]
    },
    "Audio File": "output.mp3"
}
```

---

## Assumptions & Limitations
- The **NewsAPI** key may require registration for extended usage.  
- The application processes up to **10 articles** at a time for efficiency.  
- Sentiment analysis is based on pre-trained models, which may occasionally misclassify content.  
- The Hindi TTS conversion is optimized for concise summaries and may not perform well with lengthy content.
