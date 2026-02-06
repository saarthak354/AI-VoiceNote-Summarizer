import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment, tone, and emotional shift in a voice note transcript.
    Returns structured JSON as a Python dictionary.
    """

    prompt = f"""
You are analyzing a spoken voice note transcript.

Extract the following:
1. Overall sentiment (positive, neutral, negative)
2. Tone (list of short descriptors, e.g. casual, serious, humorous)
3. Emotional shift if present (e.g. frustration → relief), or null
4. Confidence score between 0 and 1

Respond ONLY with valid JSON using this schema:
{{
  "sentiment": string,
  "tone": list[string],
  "emotional_shift": string | null,
  "confidence": number
}}

Transcript:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You extract structured emotional information from speech."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return json.loads(response.choices[0].message.content)