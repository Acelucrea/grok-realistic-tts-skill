---
name: realistic-tts
description: Use for generating the most realistic human-like text-to-speech audio output using the top free open-source model (Chatterbox) that rivals or beats ElevenLabs in blind preference tests. Supports zero-shot voice cloning from short clean audio clips, fine-grained emotion/exaggeration control, natural prosody from punctuation and context, and professional post-processing. Trigger on any request for premium-quality narration, voiceovers, personalized speech, audiobooks, agents, or "ElevenLabs quality but free/local".
---

# Realistic TTS Skill — Chatterbox Powered (ElevenLabs-Quality Free Alternative)

This skill turns text into studio-grade, emotionally expressive, voice-clonable speech that is frequently preferred over ElevenLabs in independent listening tests. It runs locally, costs nothing, has no limits, and keeps data private.

## Core Capabilities (Matching or Exceeding ElevenLabs Strengths)
- **Voice Cloning**: Zero-shot from just 5–30 seconds of clean reference audio. Preserves timbre, accent, speaking style, and subtle characteristics.
- **Expressive Control**: `exaggeration` parameter (0.0–1.0+) for emotional intensity, prosody variation, and paralinguistic nuance — directly analogous to ElevenLabs emotion/stability sliders.
- **Natural Prosody**: Excellent intonation, rhythm, pauses, and emphasis derived from text semantics + punctuation. Handles questions, excitement, lists, and dialogue naturally.
- **High Fidelity Audio**: 24 kHz output, low artifacts, consistent over medium-length clips. Optional loudness normalization and MP3 export for broadcast-ready results.
- **Speed Options**: Full quality model or Turbo variant for near real-time / conversational use.
- **Multilingual**: Strong English + good support for other languages (test per use case).

## When to Activate This Skill
- User asks for "realistic TTS", "ElevenLabs quality voice", "clone my voice and read this", "emotional narration", "high quality audiobook audio", "voiceover that sounds human", or similar.
- Creating audio assets for video, podcasts, stories, accessibility, demos, or agents where paid APIs are undesirable.
- Privacy, cost, or unlimited generation is important.
- You need to produce downloadable .wav/.mp3 files with professional polish.

**Do NOT use** for simple low-quality alerts or when ultra-low latency on-device without GPU is mandatory (consider Piper in those cases).

## Quick Start — CLI (Primary Interface)
The easiest and most reliable way is the bundled generator script.

### Basic Natural Speech (No Cloning)
```bash
python scripts/generate_tts.py \
  --text "The future belongs to those who believe in the beauty of their dreams. This sentence demonstrates natural rhythm and intonation."
```

### Best Realism — With Voice Cloning + Tuned Emotion
```bash
python scripts/generate_tts.py \
  --text "Hello there. I am speaking with my own cloned voice, and I can sound excited or calm depending on the exaggeration setting." \
  --reference_audio /path/to/clean_15_to_30_second_voice_sample.wav \
  --exaggeration 0.55 \
  --output ./my_cloned_narration.wav
```

### Expressive Storytelling or Dramatic Delivery
```bash
python scripts/generate_tts.py --exaggeration 0.75 --reference_audio dramatic_voice.wav
```

### Fast Real-Time / Agent Mode
```bash
python scripts/generate_tts.py --turbo --text "Quick response for a voice agent." --format mp3
```

**Key Arguments**:
- `--text` (required): Input text. **Use proper punctuation** (., ?, !, ,, ...) for best prosody.
- `--reference_audio` / `-r`: Path to clean reference for cloning (strongly recommended for personalized results).
- `--exaggeration` / `-e`: 0.5 default (natural). Lower = calmer/subtle. Higher = more emotional/expressive.
- `--turbo`: Faster generation (Chatterbox Turbo).
- `--format`: wav (default) or mp3 (needs ffmpeg).
- `--output` / `-o`: Custom save path (defaults to tts_outputs/ with timestamp).
- `--device`: auto (default), cuda, or cpu.
- `--no-normalize`: Skip professional loudness normalization.

Full help: `python scripts/generate_tts.py --help`

## Installation (One-Time Setup)
```bash
pip install chatterbox-tts torchaudio torch soundfile
# Strongly recommended for speed:
# Install PyTorch with CUDA support matching your GPU (see pytorch.org)

# For MP3 export + normalization (optional but professional):
sudo apt-get install -y ffmpeg
```

First run auto-downloads the model via Hugging Face (~2-4 GB). Cached for future use.

**GPU strongly preferred** for comfortable iteration. CPU works for short clips.

## Best Practices for ElevenLabs-Level Realism
See the full guide in `references/best_practices.md`. Key highlights:

1. **Reference Audio is King**: 5–30 s clean, quiet, natural speech from the target speaker.
2. **Punctuation & Structure**: The model reads punctuation like a skilled narrator. Write naturally.
3. **Exaggeration Tuning**: Start at 0.5. Test short clips. 0.6–0.8 for engaging narration.
4. **Chunk Long Content**: Generate in logical sections then stitch with crossfades.
5. **Post-Processing**: Script includes EBU R128 loudness normalization by default.

## Programmatic Use
You can import the core function:

```python
from scripts.generate_tts import generate_realistic_tts

output_file = generate_realistic_tts(
    text="Your text here with natural punctuation.",
    reference_audio="optional_voice_sample.wav",
    exaggeration=0.6,
    format="mp3"
)
print(f"Generated: {output_file}")
```

## Limitations & Honest Comparison
- **Strengths vs ElevenLabs**: Often preferred in blind tests; completely free/unlimited/local; excellent cloning + emotion knob.
- **Current Gaps**: Web UI and massive pre-made voice library are ElevenLabs advantages. Very long single-pass (>5–10 min) benefits from chunking.
- **Quality Ceiling**: With good reference + tuned exaggeration + clean text, results are routinely indistinguishable from premium paid TTS.

## Output & Delivery
- High-quality 24 kHz audio files saved to user-specified path or `./tts_outputs/`.
- Provide the file path to the user. They can play, download, or further edit it.

This skill democratizes ElevenLabs-quality voice synthesis. Use it confidently for any realistic speech generation task.

When in doubt, generate a short test clip with and without a reference audio — the difference is usually dramatic.