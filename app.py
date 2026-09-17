from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.values.get('Body', '').lower()
    r = MessagingResponse()
    m = r.message()
    if 'hi' in body or 'hello' in body:
        m.body("🙏 Gospel Bot LIVE!\n\n1 - Amazing Grace\n2 - How Great Thou Art\n\nSend 1 or 2")
    elif '1' in body:
        m.body("🎵 Amazing Grace: https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    elif '2' in body:
        m.body("🎵 How Great Thou Art: https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
    else:
        m.body("God bless! Send 'hi' to start")
    return str(r)

@app.route("/", methods=["GET"])
def home():
    return "Gospel Bot Live"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
