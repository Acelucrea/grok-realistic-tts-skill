#!/usr/bin/env python3
"""
Realistic TTS Generator using Chatterbox (most realistic free open-source model rivaling ElevenLabs)
Provides CLI and importable function for high-quality, voice-clonable, expressive speech synthesis.

Portable version for standalone use + Grok skill compatibility.
"""

import argparse
import os
import sys
import shutil
from pathlib import Path

import torch
import torchaudio as ta

try:
    from chatterbox.tts import ChatterboxTTS
    from chatterbox.tts_turbo import ChatterboxTurboTTS
except ImportError:
    print("ERROR: chatterbox-tts not installed. Run: pip install chatterbox-tts torchaudio torch")
    sys.exit(1)


def get_device(device_arg: str = "auto") -> str:
    if device_arg == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device_arg


def generate_realistic_tts(
    text: str,
    output_path: str = None,
    reference_audio: str = None,
    exaggeration: float = 0.5,
    device: str = "auto",
    use_turbo: bool = False,
    format: str = "wav",
    normalize: bool = True,
) -> str:
    """
    Generate highly realistic TTS audio using Chatterbox model.
    
    Args:
        text: The text to synthesize. Use natural punctuation for best prosody.
        output_path: Path to save the audio file. If None, saves to tts_outputs/tts_realistic_<timestamp>.wav (portable)
        reference_audio: Optional path to 5-30s clean reference audio for zero-shot voice cloning.
                         Strongly recommended for personalized, ElevenLabs-like results.
        exaggeration: Controls emotional intensity and expressiveness (0.0 = subtle/calm, 1.0+ = dramatic/emotional).
                      Default 0.5 balances naturalness and liveliness.
        device: 'cuda', 'cpu', or 'auto' (detects GPU).
        use_turbo: Use faster ChatterboxTurboTTS variant (slightly lower quality, great for real-time/agents).
        format: 'wav' (default, lossless) or 'mp3' (requires ffmpeg).
        normalize: Apply basic loudness normalization via ffmpeg if available.
    
    Returns:
        Path to the generated audio file.
    """
    device = get_device(device)
    print(f"[RealisticTTS] Using device: {device}")
    if use_turbo:
        print("[RealisticTTS] Loading Chatterbox Turbo (faster, optimized for low latency)...")
        model = ChatterboxTurboTTS.from_pretrained(device=device)
    else:
        print("[RealisticTTS] Loading Chatterbox (highest quality realistic synthesis)...")
        model = ChatterboxTTS.from_pretrained(device=device)
    
    print(f"[RealisticTTS] Model loaded. Sample rate: {model.sr} Hz")
    
    # Prepare generation kwargs
    gen_kwargs = {
        "text": text,
        "exaggeration": float(exaggeration),
    }
    
    if reference_audio:
        ref_path = Path(reference_audio)
        if not ref_path.exists():
            raise FileNotFoundError(f"Reference audio not found: {reference_audio}")
        gen_kwargs["audio_prompt_path"] = str(ref_path)
        print(f"[RealisticTTS] Using reference audio for voice cloning: {ref_path.name}")
    else:
        print("[RealisticTTS] No reference provided — using base/natural voice synthesis.")
    
    print(f"[RealisticTTS] Generating speech (exaggeration={exaggeration}) ...")
    wav = model.generate(**gen_kwargs)
    
    # Determine output path - portable default
    if output_path is None:
        # Use GROK_ARTIFACTS_DIR if set (for Grok), else ./tts_outputs
        env_dir = os.environ.get("GROK_ARTIFACTS_DIR")
        if env_dir:
            base_dir = Path(env_dir)
        else:
            base_dir = Path.cwd() / "tts_outputs"
        base_dir.mkdir(parents=True, exist_ok=True)
        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(base_dir / f"tts_realistic_{timestamp}.wav")
    else:
        output_path = str(Path(output_path).with_suffix(".wav"))
    
    output_wav = output_path if format == "wav" else str(Path(output_path).with_suffix(".wav"))
    
    ta.save(output_wav, wav, model.sr)
    print(f"[RealisticTTS] Saved WAV: {output_wav}")
    
    final_path = output_wav
    
    # Optional: Convert to MP3 and/or normalize with ffmpeg
    if format == "mp3" or normalize:
        ffmpeg_available = shutil.which("ffmpeg") is not None
        if ffmpeg_available:
            final_path = str(Path(output_path).with_suffix(f".{format}")) if format != "wav" else output_wav
            
            cmd = ["ffmpeg", "-y", "-i", output_wav]
            if normalize:
                cmd.extend(["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"])
            if format == "mp3":
                cmd.extend(["-codec:a", "libmp3lame", "-qscale:a", "2"])
            else:
                cmd.extend(["-codec:a", "copy"])
            
            cmd.append(final_path)
            
            print(f"[RealisticTTS] Post-processing with ffmpeg ({'normalize + ' if normalize else ''}{format})...")
            result = __import__("subprocess").run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[RealisticTTS] WARNING: ffmpeg failed: {result.stderr}")
                final_path = output_wav
            else:
                if format != "wav" and Path(output_wav).exists() and output_wav != final_path:
                    try:
                        os.remove(output_wav)
                    except Exception:
                        pass
                print(f"[RealisticTTS] Final output: {final_path}")
        else:
            print("[RealisticTTS] WARNING: ffmpeg not found. Install for MP3 conversion and normalization. Falling back to WAV.")
            final_path = output_wav
    
    print(f"[RealisticTTS] ✅ Done! Audio ready at: {final_path}")
    print(f"   Duration: ~{len(wav[0]) / model.sr:.1f} seconds | Quality: 24kHz realistic speech")
    return final_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate the most realistic TTS audio using Chatterbox (free ElevenLabs alternative with voice cloning & emotion control)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic natural speech
  python generate_tts.py --text "The quick brown fox jumps over the lazy dog. This demonstrates natural prosody."

  # With voice cloning (best realism)
  python generate_tts.py --text "Hello, this is my cloned voice speaking naturally." \
    --reference_audio /path/to/my_voice_sample.wav --exaggeration 0.55

  # Expressive narration
  python generate_tts.py --text "Once upon a time, in a land far away..." \
    --exaggeration 0.75 --output ./story.wav

  # Fast turbo mode for agents
  python generate_tts.py --text "Real-time response here." --use_turbo --format mp3
"""
    )
    parser.add_argument("--text", type=str, required=True, help="Text to convert to speech. Use punctuation for natural intonation.")
    parser.add_argument("--output", "-o", type=str, default=None, help="Output audio path (default: ./tts_outputs/tts_realistic_YYYYMMDD_HHMMSS.wav)")
    parser.add_argument("--reference_audio", "-r", type=str, default=None, help="Path to clean 5-30 second reference audio file for zero-shot voice cloning (recommended for best personalized results).")
    parser.add_argument("--exaggeration", "-e", type=float, default=0.5, help="Emotional expressiveness (0.0 subtle to 1.0+ dramatic). Default 0.5 = natural conversational.")
    parser.add_argument("--device", type=str, default="auto", choices=["auto", "cuda", "cpu"], help="Inference device.")
    parser.add_argument("--turbo", "--use_turbo", dest="use_turbo", action="store_true", help="Use faster Turbo variant (good for real-time, slightly less peak quality).")
    parser.add_argument("--format", type=str, default="wav", choices=["wav", "mp3"], help="Output format. mp3 requires ffmpeg.")
    parser.add_argument("--no-normalize", dest="normalize", action="store_false", help="Disable loudness normalization (enabled by default for pro sound).")
    
    args = parser.parse_args()
    
    if not args.text.strip():
        print("ERROR: --text cannot be empty.")
        sys.exit(1)
    
    try:
        output_file = generate_realistic_tts(
            text=args.text,
            output_path=args.output,
            reference_audio=args.reference_audio,
            exaggeration=args.exaggeration,
            device=args.device,
            use_turbo=args.use_turbo,
            format=args.format,
            normalize=args.normalize,
        )
        print(f"\n\ud83c\udf99\ufe0f  Realistic TTS complete. File: {output_file}")
    except Exception as exc:
        print(f"ERROR: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
