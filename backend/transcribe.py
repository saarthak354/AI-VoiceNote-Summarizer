from pathlib import Path
import whisper

from preprocessing import preprocess_audio
from sentiment import analyze_sentiment
from intent import extract_intent
from summarization import summarize_transcript
from chunking import get_audio_duration
from long_audio import process_long_audio


# --------------------
# Configuration
# --------------------

ENABLE_SENTIMENT = True
ENABLE_SUMMARIZATION = True

LONG_AUDIO_THRESHOLD_SECONDS = 8 * 60  # 8 minutes
MODEL_SIZE = "medium"

AUDIO_DIR = Path("backend/audio")


# Load Whisper ONCE
WHISPER_MODEL = whisper.load_model(MODEL_SIZE)


def transcribe_audio(audio_path: Path):
    """
    Handles short audio files (below long-audio threshold).
    """

    print(f"Processing short audio: {audio_path.name}")

    clean_audio = preprocess_audio(audio_path)

    result = WHISPER_MODEL.transcribe(str(clean_audio), fp16=False)
    transcript_text = result["text"].strip()

    print("\n--- TRANSCRIPT START ---\n")
    print(transcript_text)
    print("\n--- TRANSCRIPT END ---\n")

    sentiment = None
    intent = None

    if ENABLE_SENTIMENT:
        sentiment = analyze_sentiment(transcript_text)
        intent = extract_intent(transcript_text)

    if ENABLE_SUMMARIZATION:
        summary = summarize_transcript(
            transcript_text,
            sentiment=sentiment,
            intent=intent
        )

        print("\n--- TL;DR ---\n")
        print(summary["tldr"])

        print("\n--- DETAILED SUMMARY ---\n")
        print(summary["detailed_summary"])


# --------------------
# Entry point
# --------------------

if __name__ == "__main__":
    audio_files = list(AUDIO_DIR.glob("*"))

    if not audio_files:
        print("No audio files found in backend/audio")
        exit(0)

    audio_path = audio_files[0]
    duration = get_audio_duration(audio_path)

    if duration <= LONG_AUDIO_THRESHOLD_SECONDS:
        transcribe_audio(audio_path)
    else:
        summary = process_long_audio(audio_path)

        print("\n--- TL;DR ---\n")
        print(summary["tldr"])

        print("\n--- DETAILED SUMMARY ---\n")
        print(summary["detailed_summary"])