#This will handle recording and transcription



# whisper_utils.py

import os
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("api_keys.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def record_audio(duration=5, fs=44100):
    print("[MIC] Recording for", duration, "seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio, fs

def save_temp_wav(audio, fs):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, fs, audio)
    print(f"[MIC] Saved temporary WAV file: {temp_file.name}")
    return temp_file.name

def transcribe_audio(file_path):
    print("[WHISPER] Sending audio to Whisper...")
    try:
        with open(file_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return transcript.text.strip()
    except Exception as e:
        print(f"[WHISPER ERROR] {e}")
        return "Error during transcription"

def record_and_transcribe():
    audio, fs = record_audio()
    wav_path = save_temp_wav(audio, fs)
    text = transcribe_audio(wav_path)
    os.remove(wav_path)  # Cleanup temp file
    print(f"[WHISPER] Transcription: {text}")
    return text
