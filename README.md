# AI-VoiceNote-Summarizer

This project is an experimental AI pipeline that converts voice notes into:
- a raw transcript
- a concise TL;DR
- a detailed summary

---

 ## What It Does (Current State)

Given an audio file (`.mp3`):
1. Transcribes speech to text using **OpenAI Whisper**
2. Outputs the **raw transcript** (no heavy cleaning)
3. Generates:
   - a **TL;DR** summary
   - a **detailed summary**
   using a transformer-based summarization model

The pipeline runs **locally** on CPU (no cloud APIs).

---



## Tech Stack

- **Python 3.11**
- **Whisper** — speech-to-text
- **Hugging Face Transformers**
  - BART / DistilBART for summarization
- **ffmpeg** — audio processing

---

## Known Limitations (Important)

This project is **not yet production-ready**.

Current issues and limitations:
- Summarization quality degrades on very short or purely instructional audio
- Long audio (> a few minutes) is not fully supported yet
- Summarization models may add redundant or unnecessary phrasing
- No action item extraction (e.g., tasks, deadlines)
- No content-type detection (commands vs narrative speech)
- No confidence scoring or reliability indicators

These limitations are intentional and documented for future refinement.


## Planned Improvements (Roadmap)

- Hierarchical summarization for long audio
  - chunk audio → summarize chunks → summarize summaries
- Content-type–aware handling
  - different logic for commands, notifications, meetings, lectures
- Action item extraction (deadlines, tasks, requests)
- Better length-adaptive summarization policies
- Cleaner separation of pipeline stages in code
- Optional lightweight UI / CLI improvements

---
