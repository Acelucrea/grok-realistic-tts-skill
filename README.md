# grok-realistic-tts-skill

**The most realistic free open-source Text-to-Speech skill for Grok (and standalone use)** — powered by [Chatterbox](https://github.com/resemble-ai/chatterbox) from Resemble AI.

Chatterbox frequently outperforms or matches ElevenLabs in blind listening tests while being completely free, local, unlimited, and private.

## ✨ Key Features

- **Zero-shot Voice Cloning**: Clone any voice from just 5–30 seconds of clean reference audio.
- **Expressive Control**: Fine-grained `exaggeration` parameter for emotion, prosody, and style (analogous to ElevenLabs sliders).
- **Natural Prosody**: Excellent intonation, rhythm, pauses, and emphasis from text semantics + punctuation.
- **High-Fidelity Output**: 24 kHz studio-quality audio with optional EBU R128 loudness normalization and MP3 export.
- **Fast & Flexible**: Full-quality or Turbo mode for real-time/agent use. CLI + importable Python API.
- **Best Practices Included**: Comprehensive guide adapted from premium TTS workflows.

## 🚀 Quick Start (Standalone)

### 1. Installation
```bash
pip install chatterbox-tts torchaudio torch soundfile

# For MP3 export and professional normalization (recommended)
sudo apt-get install -y ffmpeg

# GPU support (strongly recommended)
# See https://pytorch.org/get-started/locally/
```

First run downloads the model (~2-4 GB) from Hugging Face.

### 2. Generate Audio

**Basic natural speech:**
```bash
python scripts/generate_tts.py --text "The future belongs to those who believe in the beauty of their dreams. This demonstrates natural rhythm and intonation."
```

**Best realism — clone your voice:**
```bash
python scripts/generate_tts.py \
  --text "Hello there. I am speaking with my own cloned voice..." \
  --reference_audio /path/to/your_clean_15-30s_voice_sample.wav \
  --exaggeration 0.55 \
  --output ./my_narration.wav
```

**Expressive or dramatic delivery:**
```bash
python scripts/generate_tts.py --text "Once upon a time..." --exaggeration 0.75
```

**Fast mode for agents/real-time:**
```bash
python scripts/generate_tts.py --text "Quick response." --turbo --format mp3
```

See `python scripts/generate_tts.py --help` for all options.

## 📦 As a Grok Skill

This project is also a ready-to-use custom skill for xAI Grok.

Copy the folder to your Grok skills directory (usually `~/.grok/skills/` or equivalent) and activate it when you need premium realistic TTS.

Trigger phrases: "realistic TTS", "ElevenLabs quality voice", "clone my voice and read this", "emotional narration", etc.

Full skill documentation is in `SKILL.md`.

## 📖 Documentation

- [SKILL.md](SKILL.md) — Grok skill definition and usage instructions
- [references/best_practices.md](references/best_practices.md) — Detailed guide for achieving ElevenLabs-level results (reference audio, prosody, exaggeration tuning, troubleshooting)
- `scripts/generate_tts.py` — Full-featured CLI and Python function

## 🛠️ Project Structure
```
grok-realistic-tts-skill/
├── README.md
├── LICENSE
├── .gitignore
├── SKILL.md                 # For Grok integration
├── scripts/
│   └── generate_tts.py      # Main generator (CLI + API)
└── references/
    └── best_practices.md    # In-depth realism guide
```

## 🔄 Comparison to ElevenLabs

| Aspect              | Chatterbox (this skill)      | ElevenLabs              |
|---------------------|------------------------------|-------------------------|
| Cost                | Free + unlimited            | Paid (credits)         |
| Privacy             | 100% local                  | Cloud                  |
| Voice Cloning       | Excellent zero-shot         | Excellent              |
| Expressiveness      | Strong via exaggeration     | Very strong            |
| Blind Test Results  | Often preferred             | Industry benchmark     |
| Setup               | One-time pip + model download | Instant web/app       |

Many users find the output indistinguishable for narration, podcasts, and personal use.

## 📜 License

MIT License — free for personal and commercial use.

## 🙏 Credits

- Core model: [Chatterbox by Resemble AI](https://github.com/resemble-ai/chatterbox)
- Original research & inspiration: ElevenLabs for setting the quality bar
- Built as a custom skill for xAI Grok

---

**Ready to generate voices that sound truly human?** Start with a clean reference clip and natural text — the results will surprise you.