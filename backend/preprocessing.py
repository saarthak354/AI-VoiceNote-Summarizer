from pathlib import Path
import subprocess

TEMP_DIR = Path("backend/tmp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def preprocess_audio(input_path: Path) -> Path:
    
    output_path = TEMP_DIR / f"{input_path.stem}_clean.wav"

    command = [
        "ffmpeg",
        "-y",                  # overwrite output if it exists
        "-i", str(input_path), # input audio file
        "-ac", "1",            # force mono
        "-ar", "16000",        # resample to 16kHz
        str(output_path)
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return output_path