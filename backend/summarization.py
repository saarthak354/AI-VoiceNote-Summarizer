import os
import json
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None


def summarize_transcript(
    text: str,
    sentiment: dict | None = None,
    intent: dict | None = None
) -> dict:
    """
    Generate a TL;DR and a detailed summary from a voice note transcript.
    Conditions silently on sentiment and intent.
    """

    if client is None:
        raise RuntimeError("OPENAI_API_KEY not set. Summarization disabled.")

    sentiment_context = ""
    if sentiment:
        sentiment_context = f"""
Sentiment context (internal):
- Overall sentiment: {sentiment.get("sentiment")}
- Tone: {", ".join(sentiment.get("tone", []))}
- Emotional shift: {sentiment.get("emotional_shift")}
"""

    intent_context = ""
    if intent:
        intent_context = f"""
Intent context (internal):
- Primary intent: {intent.get("intent")}
- Urgency: {intent.get("urgency")}
- Action items present: {len(intent.get("action_items", [])) > 0}
"""

    prompt = f"""
You are summarizing a spoken voice note.

{sentiment_context}
{intent_context}

Instructions:
- Write a concise TL;DR (1–2 sentences).
- Write a detailed summary that preserves intent and emotional nuance.
- Do NOT invent tasks, deadlines, or decisions.
- Do NOT mention sentiment or intent explicitly.
- Keep the language natural and human.

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
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)