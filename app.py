# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import gradio as gr
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from gtts import gTTS
from deep_translator import GoogleTranslator
from keybert import KeyBERT
import json

app = FastAPI()
kw_model = KeyBERT()

def extract_news(company_name):
    url = f'https://newsapi.org/v2/everything?q={company_name}&apiKey= I have hidden my private api key'
    response = requests.get(url).json()
    articles = response.get('articles', [])[:10]
    extracted_data = []

    for article in articles:
        extracted_data.append({
            'title': article['title'],
            'summary': article['description'] or 'No summary available',
            'content': article['content'] or 'No content available'
        })

    return extracted_data

def extract_topics(articles):
    for article in articles:
        content = article['content'] if article['content'] != 'No content available' else ''
        article['topics'] = kw_model.extract_keywords(content, keyphrase_ngram_range=(1, 2), stop_words='english')
    return articles

def analyze_sentiment(articles):
    sentiment_pipeline = pipeline("sentiment-analysis")
    for article in articles:
        if article['content'] != 'No content available':
            result = sentiment_pipeline(article['content'])[0]
            article['sentiment'] = result['label']
        else:
            article['sentiment'] = 'NEUTRAL'
    return articles

def comparative_analysis(articles):
    positive = sum(1 for a in articles if a['sentiment'] == 'POSITIVE')
    negative = sum(1 for a in articles if a['sentiment'] == 'NEGATIVE')
    neutral = len(articles) - positive - negative

    all_topics = [topic for article in articles for topic in article['topics']]
    unique_topics = set(all_topics)

    return {
        'Sentiment Distribution': {'Positive': positive, 'Negative': negative, 'Neutral': neutral},
        'Unique Topics': list(unique_topics),
        'Coverage Differences': [
            {
                'Comparison': 'Positive articles highlight company achievements, while Negative articles focus on concerns.',
                'Impact': 'Mixed reviews may influence investor sentiment.'
            }
        ]
    }

def generate_summary(positive, negative):
    if positive > negative:
        return "Overall sentiment is positive, indicating positive market perception."
    elif negative > positive:
        return "Overall sentiment is negative, which may influence investor confidence."
    else:
        return "Overall sentiment is neutral with mixed opinions."

def text_to_speech(text, filename="output.mp3"):
    if not text.strip():
        text = "कोई सारांश उपलब्ध नहीं है।"

    translated_text = GoogleTranslator(source='auto', target='hi').translate(text)

    tts = gTTS(translated_text, lang='hi')
    tts.save(filename)
    return filename

def main(company_name):
    articles = extract_news(company_name)
    articles = extract_topics(articles)
    analyzed_articles = analyze_sentiment(articles)
    comparison = comparative_analysis(analyzed_articles)
    sentiment_summary = generate_summary(comparison['Sentiment Distribution']['Positive'],
                                         comparison['Sentiment Distribution']['Negative'])

    summary = "\n".join([f"{a['title']}: {a['sentiment']}" for a in analyzed_articles if a['content'] != 'No content available'])
    audio_file = text_to_speech(summary)

    result = {
        'Company': company_name,
        'Articles': analyzed_articles,
        'Comparative Sentiment Score': comparison,
        'Final Sentiment Summary': sentiment_summary,
        'Audio File': audio_file
    }

    return result

@app.get("/analyze")
async def analyze(company_name: str):
    result = main(company_name)
    return JSONResponse(content=result)

def gradio_interface(company_name):
    result = main(company_name)
    return json.dumps(result, indent=4, ensure_ascii=False), result['Audio File']

iface = gr.Interface(fn=gradio_interface, inputs="text", outputs=["text", "audio"],
                     title="News Summarization and Sentiment Analysis")

iface.launch()
