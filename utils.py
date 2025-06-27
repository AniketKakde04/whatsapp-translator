import os
import requests
from pydub import AudioSegment
from google import genai

client = genai.Client()

def transcribe_and_translate(media_url):
    try:
        # Step 1: Download the audio
        audio_ogg = "audio.ogg"
        audio_wav = "audio.wav"
        r = requests.get(media_url)
        with open(audio_ogg, "wb") as f:
            f.write(r.content)

        # Step 2: Convert OGG to WAV using pydub
        audio = AudioSegment.from_file(audio_ogg)
        audio.export(audio_wav, format="wav")

        # Step 3: Upload to Gemini and translate
        upload = client.files.upload(file=audio_wav)
        prompt = (
            "Transcribe and translate this audio file:\n"
            "1. Transcription in original language.\n"
            "2. English translation."
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, upload]
        )

        return response.text.strip()

    except Exception as e:
        print("ERROR:", e)
        return "❌ Error processing the voice note."
