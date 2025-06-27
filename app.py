from flask import Flask, request, Response
from utils import transcribe_and_translate
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From")
    media_url = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0")

    print("Media URL:", media_url)
    print("Media Type:", media_type)

    # Only accept MP3 or WAV
    if media_url and media_type in ["audio/mpeg", "audio/wav"]:
        reply = transcribe_and_translate(media_url)
    else:
        reply = (
            "❗ Voice notes (.ogg) are not supported.\n\n"
            "Please send an audio file in `.mp3` or `.wav` format instead."
        )

    return Response(f"""
        <Response>
            <Message to="{from_number}">{reply}</Message>
        </Response>
    """, mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
