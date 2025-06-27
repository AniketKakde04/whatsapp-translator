from flask import Flask, request, Response
from utils import transcribe_and_translate
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    from_number = request.form.get("From")
    media_url = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0")

    if media_url and "audio" in media_type:
        reply = transcribe_and_translate(media_url)
    else:
        reply = "Please send a voice note."

    return Response(f"""
        <Response>
            <Message to="{from_number}">{reply}</Message>
        </Response>
    """, mimetype="text/xml")

if __name__ == "__main__":
    app.run()
