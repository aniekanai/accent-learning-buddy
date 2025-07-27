# GUI app for accent learning buddy


import tkinter as tk
from tkinter import ttk
from tts_utils import play_text
from whisper_utils import record_and_transcribe
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv("api_keys.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# Tkinter Setup
# -----------------------------
root = tk.Tk()
root.title("Accent Learning Buddy")
root.geometry("500x400")
root.configure(bg="white")

# -----------------------------
# Variables
# -----------------------------
selected_accent = tk.StringVar()
selected_mode = tk.StringVar()
target_phrase = tk.StringVar()
feedback_text = tk.StringVar()
transcribed_attempt = tk.StringVar()

# -----------------------------
# Dropdowns
# -----------------------------
ttk.Label(root, text="Select Accent:").pack(pady=(10, 0))
accent_dropdown = ttk.Combobox(root, textvariable=selected_accent, state="readonly")
accent_dropdown['values'] = ["American", "British", "Australian", "Roadman"]
accent_dropdown.current(0)
accent_dropdown.pack()

ttk.Label(root, text="Select Mode:").pack(pady=(10, 0))
mode_dropdown = ttk.Combobox(root, textvariable=selected_mode, state="readonly")
mode_dropdown['values'] = ["Accent", "Conversation", "Vocabulary"]
mode_dropdown.current(0)
mode_dropdown.pack()

# -----------------------------
# Phrase Display
# -----------------------------
ttk.Label(root, text="Target Phrase:").pack(pady=(15, 0))
phrase_label = ttk.Label(root, textvariable=target_phrase, wraplength=400)
phrase_label.pack()

# -----------------------------
# Feedback Display
# -----------------------------
ttk.Label(root, text="Feedback:").pack(pady=(15, 0))
feedback_label = ttk.Label(root, textvariable=feedback_text, wraplength=400, foreground="green")
feedback_label.pack()

# -----------------------------
# Core Functions
# -----------------------------
def generate_phrase():
    accent = selected_accent.get()
    mode = selected_mode.get()

    prompt = f"Give me a short, natural-sounding English sentence that reflects a {accent} accent style. Keep it under 10 words. Mode: {mode}"
    print(f"[GENERATION] Prompting: {prompt}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        phrase = response.choices[0].message.content.strip()
        target_phrase.set(phrase)
    except Exception as e:
        target_phrase.set("Error generating phrase.")
        print(f"[GENERATION ERROR] {e}")

def play_phrase():
    phrase = target_phrase.get()
    if phrase:
        play_text(phrase)

def record_attempt():
    transcription = record_and_transcribe()
    transcribed_attempt.set(transcription)

def generate_feedback():
    original = target_phrase.get()
    attempt = transcribed_attempt.get()

    if not attempt:
        feedback_text.set("Please record your attempt first.")
        return

    prompt = f"The user tried to repeat: \"{original}\" but said: \"{attempt}\". Give short, specific pronunciation or tone feedback in one sentence."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        feedback = response.choices[0].message.content.strip()
        feedback_text.set(feedback)
    except Exception as e:
        feedback_text.set("Error generating feedback.")
        print(f"[FEEDBACK ERROR] {e}")

def play_feedback():
    feedback = feedback_text.get()
    if feedback:
        play_text(feedback)

# -----------------------------
# Buttons
# -----------------------------
ttk.Button(root, text="▶ Generate Phrase", command=generate_phrase).pack(pady=5)
ttk.Button(root, text="🔊 Play Phrase", command=play_phrase).pack(pady=5)
ttk.Button(root, text="🎙️ Record Attempt", command=record_attempt).pack(pady=5)
ttk.Button(root, text="✅ Get Feedback", command=generate_feedback).pack(pady=5)
ttk.Button(root, text="🔁 Play Feedback", command=play_feedback).pack(pady=5)

# -----------------------------
# Run App
# -----------------------------
root.mainloop()
