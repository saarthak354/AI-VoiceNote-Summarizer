# AI Voice Note Summarizer  
**Phase 1 — Speech-to-Text & Intelligence Foundation**

This project is an experimental AI pipeline that processes real-world voice notes
(e.g. WhatsApp recordings) into high-quality transcripts and extracts
foundational signals required for downstream summarization and understanding.

The current focus is on **robust audio ingestion and accurate speech-to-text** —
the most critical prerequisite for reliable summarization.

---

## What It Does (Current State)

Given an audio file (`.opus`, `.ogg`, `.mp3`, `.m4a`):

1. **Preprocesses audio** using ffmpeg  
   - Converts to mono  
   - Resamples to 16 kHz (Whisper-friendly format)

2. **Transcribes speech to text** using OpenAI Whisper (`medium` model)  
   - Optimized for conversational speech and varied accents  
   - Runs locally on CPU (no cloud ASR APIs)

3. **Outputs a clean raw transcript**  
   - Printed directly to the terminal  
   - No aggressive post-processing (intentional)

This repository currently implements the **ASR and preprocessing foundation**
for a voice note summarization system.

---

## Why This Design

High-quality summarization is impossible without high-quality transcripts.

This project intentionally prioritizes:
- real-world audio formats (e.g. WhatsApp `.opus`)
- deterministic preprocessing
- transcription accuracy over speed
- clean, modular pipeline design

Summarization and higher-level understanding are built **on top of this foundation**
in later phases.

---

## Tech Stack

- **Python 3.11+**
- **OpenAI Whisper** — speech-to-text (medium model)
- **ffmpeg** — audio preprocessing
- **Local CPU execution** (no ASR cloud APIs)

---

## Project Structure

```text
backend/
├── audio/          # Input audio files
├── tmp/            # Temporary preprocessed audio
├── transcripts/    # Generated transcripts (optional)
├── preprocessing.py
└── transcribe.py