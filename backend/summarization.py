import os
import json
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None


def summarize_transcript(
    text: str,
    sentiment: dict | None = None
) -> dict:
    """
    Generate a TL;DR and a detailed summary from a voice note transcript.
    Optionally conditions on sentiment and emotional tone.
    """

    if client is None:
        raise RuntimeError("OPENAI_API_KEY not set. Summarization disabled.")

    sentiment_context = ""
    if sentiment:
        sentiment_context = f"""
Sentiment context:
- Overall sentiment: {sentiment.get("sentiment")}
- Tone: {", ".join(sentiment.get("tone", []))}
- Emotional shift: {sentiment.get("emotional_shift")}
"""

    prompt = f"""
You are summarizing a spoken voice note.

Guidelines:
- Do NOT add information not present in the transcript
- Preserve the speaker's intent and emotional context
- Be concise and concrete

{sentiment_context}

Return ONLY valid JSON in this format:
{{
  "tldr": string,
  "detailed_summary": string
}}

Transcript:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You generate precise summaries of spoken content."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)