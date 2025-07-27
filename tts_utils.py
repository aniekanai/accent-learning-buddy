#This will handle Murf TTS and OpenAI feedback

import os
from murf import Murf
from dotenv import load_dotenv
import pygame
import time

load_dotenv("api_keys.env")

MURF_API_KEY = os.getenv("MURF_API_KEY")
murf_client = Murf(api_key=MURF_API_KEY)



def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def play_text(text):
    try:
        print(f"[TTS] Generating audio for: {text}")
        audio_stream = murf_client.text_to_speech.stream(
            text=text,
            voice_id="en-US-ariana",
            format="MP3",
            style="Conversational",
            pitch=0
        )
        
        output_path = "output.mp3"

        # ✅ Delete file if it exists to avoid "Permission denied"
        if os.path.exists(output_path):
            os.remove(output_path)
            
        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

        print("[TTS] Playing audio...")
        play_audio(output_path)

    except Exception as e:
        print(f"[TTS] Error: {e}")
