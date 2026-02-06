# AI-VoiceNote-Summarizer

AI-VoiceNote-Summarizer is a local-first AI system that converts voice notes into structured understanding and high-quality summaries.

Given a voice note, the system:
- transcribes speech to text
- understands sentiment and intent
- extracts actionable meaning
- produces concise and detailed summaries
- scales reliably from short notes to long (30+ minute) audio

The pipeline is designed with clear separation between audio processing, language understanding, and orchestration.

---

## What It Does

### Short Audio (≤ ~8 minutes)

For short voice notes, the system:
1. Transcribes speech using **OpenAI Whisper**
2. Analyzes sentiment and emotional tone
3. Extracts speaker intent and explicit action items
4. Generates:
   - a **TL;DR**
   - a **detailed summary**

---

### Long Audio (Meetings, Lectures, Podcasts)

For long audio, the system automatically switches to a hierarchical pipeline:

1. Splits audio into overlapping 5-minute chunks
2. Processes each chunk independently:
   - transcription
   - sentiment analysis
   - intent extraction
   - micro-summarization
3. Aggregates chunk-level understanding
4. Produces a coherent global:
   - **TL;DR**
   - **detailed summary**

This design avoids loss of structure, reduces hallucination, and preserves narrative flow across long recordings.

---

## Example Output

**Transcript (excerpt):**
> The train was already moving when he realized his ticket was for yesterday…

**Sentiment & Intent (internal):**
- Sentiment: neutral → acceptance  
- Intent: reflective  
- Action items: none  

**TL;DR:**
> A man boards a train with the wrong ticket, considers fixing the mistake, but ultimately chooses acceptance and moves forward.

**Detailed Summary:**
> Realizing his ticket was for the wrong day, he still boards the train and observes the world passing by…

---

## Architecture Overview
audio
├── preprocessing (ffmpeg)
├── transcription (Whisper)
├── sentiment analysis
├── intent extraction
├── summarization
└── orchestration
├── short-audio path
└── long-audio (hierarchical) path


Each stage is implemented as an independent module to keep the system testable and extensible.

---

## Tech Stack

- **Python 3.11+**
- **OpenAI Whisper** — speech-to-text
- **OpenAI GPT-4.1-mini** — sentiment, intent, summarization
- **ffmpeg / ffprobe** — audio preprocessing and chunking
- **Local execution** — no cloud storage or external pipelines

---

## Project Structure
backend/
├── preprocessing.py     # audio normalization
├── chunking.py          # duration detection & chunking
├── long_audio.py        # hierarchical orchestration
├── sentiment.py         # sentiment & tone analysis
├── intent.py            # intent & action extraction
├── summarization.py     # TL;DR & detailed summaries
├── transcribe.py        # entry point & routing


---

## Design Principles

- **Local-first**: audio is processed locally
- **Deterministic routing**: audio length decides pipeline path
- **Separation of concerns**: no monolithic scripts
- **Conservative extraction**: silence is preferred over hallucination
- **Scalable reasoning**: long audio handled via hierarchy, not brute force

---

## Known Limitations

- Speaker diarization is not supported yet
- Deadlines are extracted only when explicitly stated
- No UI (CLI-only for now)
- Calendar integrations are not implemented yet
- Chunk aggregation is semantic, not speaker-aware

---

## Roadmap

### Phase 5 (Planned)

- Deadline normalization (relative → absolute)
- Optional calendar integration (e.g., Google Calendar) with user confirmation
- Improved long-audio aggregation strategies
- CLI improvements and configuration flags

---

## Status

**Current Phase:**  
✔ Phase 4 — Hierarchical long-audio summarization

The core intelligence pipeline is complete and extensible.