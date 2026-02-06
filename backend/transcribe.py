from pathlib import Path
import whisper
from preprocessing import preprocess_audio

AUDIO_DIR = Path("backend/audio")
TRANSCRIPT_DIR = Path("backend/transcripts")

TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_SIZE = "medium"


def transcribe_audio(audio_path: Path):
    """
    Preprocesses audio and transcribes it using Whisper.
    """

    print(f"Processing: {audio_path.name}")

    # Step 1: clean the audio
    clean_audio = preprocess_audio(audio_path)

    # Step 2: load Whisper model
    model = whisper.load_model(MODEL_SIZE)

    # Step 3: transcribe
    result = model.transcribe(str(clean_audio), fp16=False)

    # Step 4: save transcript
    print("\n--- TRANSCRIPT START ---\n")
    print(result["text"])
    print("\n--- TRANSCRIPT END ---\n")


if __name__ == "__main__":
    audio_files = list(AUDIO_DIR.glob("*"))

    if not audio_files:
        print("No audio files found in backend/audio")
    else:
        transcribe_audio(audio_files[0])