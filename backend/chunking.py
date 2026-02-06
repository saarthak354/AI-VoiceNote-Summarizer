from pathlib import Path
import subprocess
import math

TMP_DIR = Path("backend/tmp")
TMP_DIR.mkdir(parents=True, exist_ok=True)


def get_audio_duration(audio_path: Path) -> float:
    """
    Returns audio duration in seconds using ffprobe.
    """

    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return float(result.stdout.strip())


def split_audio_into_chunks(
    audio_path: Path,
    chunk_seconds: int = 300,
    overlap_seconds: int = 15
) -> list[Path]:
    """
    Splits audio into fixed-length chunks with overlap.
    Returns a list of chunk file paths.
    """

    duration = get_audio_duration(audio_path)
    chunks = []

    step = chunk_seconds - overlap_seconds
    total_chunks = math.ceil(duration / step)

    for i in range(total_chunks):
        start_time = i * step
        output_path = TMP_DIR / f"{audio_path.stem}_chunk_{i}.wav"

        command = [
            "ffmpeg",
            "-y",
            "-i", str(audio_path),
            "-ss", str(start_time),
            "-t", str(chunk_seconds),
            "-ac", "1",
            "-ar", "16000",
            str(output_path)
        ]

        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        chunks.append(output_path)

    return chunks