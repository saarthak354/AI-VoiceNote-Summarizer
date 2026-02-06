from pathlib import Path

from chunking import get_audio_duration, split_audio_into_chunks
from preprocessing import preprocess_audio
import whisper

from sentiment import analyze_sentiment
from intent import extract_intent
from summarization import summarize_transcript


LONG_AUDIO_THRESHOLD_SECONDS = 8 * 60  # 8 minutes
WHISPER_MODEL_SIZE = "medium"


def process_long_audio(audio_path: Path) -> dict:
    """
    Processes long audio by:
    - chunking
    - understanding each chunk
    - aggregating meaning
    - producing a final summary
    """

    print(f"Processing long audio: {audio_path.name}")

    # 1. Split into chunks
    chunks = split_audio_into_chunks(audio_path)

    model = whisper.load_model(WHISPER_MODEL_SIZE)

    chunk_summaries = []
    all_actions = []
    intents = []
    sentiments = []

    # 2. Process each chunk independently
    for idx, chunk_path in enumerate(chunks):
        print(f"  → Chunk {idx + 1}/{len(chunks)}")

        clean_chunk = preprocess_audio(chunk_path)

        result = model.transcribe(str(clean_chunk), fp16=False)
        text = result["text"].strip()

        if not text:
            continue

        sentiment = analyze_sentiment(text)
        intent = extract_intent(text)

        micro_summary = summarize_transcript(
            text,
            sentiment=sentiment,
            intent=intent
        )

        chunk_summaries.append(
            {
                "index": idx,
                "summary": micro_summary["detailed_summary"],
            }
        )

        sentiments.append(sentiment.get("sentiment"))
        intents.append(intent.get("intent"))
        all_actions.extend(intent.get("action_items", []))

    # 3. Aggregate understanding across chunks
    aggregated_text = "\n".join(
        f"- {c['summary']}" for c in chunk_summaries
    )

    dominant_intent = max(set(intents), key=intents.count) if intents else None
    dominant_sentiment = max(set(sentiments), key=sentiments.count) if sentiments else None

    # 4. Final summarization pass
    final_summary = summarize_transcript(
        aggregated_text,
        sentiment={"sentiment": dominant_sentiment} if dominant_sentiment else None,
        intent={"intent": dominant_intent, "action_items": all_actions} if dominant_intent else None
    )

    return final_summary