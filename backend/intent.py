import os
import json
from openai import OpenAI

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None


def summarize_transcript(text: str, sentiment: dict | None = None, intent: dict | None = None) -> dict:
    """
    Classifies the intent of a voice note and extracts
    action items or decisions if present.

    Returns structured JSON following the intent schema.
    """

    if client is None:
        raise RuntimeError("OPENAI_API_KEY not set. Intent extraction disabled.")

    prompt = f"""
You are analyzing a spoken voice note transcript.

Your task:
1. Identify the PRIMARY intent of the voice note.
2. Extract action items ONLY if they are explicit and high-confidence.
3. Extract decisions ONLY if a clear choice was made.
4. If unsure, leave fields empty instead of guessing.

Allowed intent values:
- task
- decision
- reflection
- idea
- story
- vent
- mixed

Rules:
- Do NOT invent tasks.
- Do NOT infer deadlines unless explicitly stated.
- If one or more action_items are present, intent MUST be "task" or "mixed".
- Silence is better than a wrong extraction.
- If a relative time reference like "tomorrow" or "tonight" is explicitly stated,
  it may be used as a deadline string.

Return ONLY valid JSON using this exact schema:
{{
  "intent": string,
  "confidence": number,
  "action_items": [
    {{
      "task": string,
      "deadline": string | null,
      "confidence": number
    }}
  ],
  "decisions": [string],
  "urgency": "none | low | medium | high"
}}

Transcript:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You extract intent and actionable meaning from spoken language."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)