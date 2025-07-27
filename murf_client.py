# Murf API Integration



import requests
from config import MURF_API_KEY

class MurfClient:
    BASE_URL = "https://api.murf.ai/v1"

    def __init__(self, api_key=MURF_API_KEY):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def stream_text_to_speech(self, text, output_path, voice_id="en-US-ariana", style="Conversational"):
        try:
            url = f"{self.BASE_URL}/speech/generate-stream"
            payload = {
                "voice_id": voice_id,
                "text": text,
                "format": "mp3",
                "style": style,
                "pitch": 0
            }

            with requests.post(url, json=payload, headers=self.headers, stream=True) as r:
                r.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print(f"Audio saved to {output_path}")

        except Exception as e:
            print(f"Error generating speech: {e}")
