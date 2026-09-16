import os
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "gospel123")
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")

SONGS = [
    {"title": "Way Maker", "artist": "Sinach"},
    {"title": "Excess Love", "artist": "Mercy Chinwo"},
    {"title": "You Are The Reason", "artist": "Calum Scott"},
    {"title": "What A Beautiful Name", "artist": "Hillsong"},
    {"title": "Goodness of God", "artist": "Bethel Music"},
]

def search_songs(query):
    query = query.lower().strip()

    if query in ["hi", "hello", "hey", "list", "songs"]:
        result_str = "🎵 **Available Songs:**\n"
        for s in SONGS:
            result_str += f"- {s['title']} by {s['artist']}\n"
        result_str += "\nType a song name to search!"
        return result_str

    results = [
        s for s in SONGS
        if query in s["title"].lower() or query in s["artist"].lower()
    ]

    if results:
        result_str = "🎵 **Search Results:**\n"
        for s in results:
            result_str += f"- *{s['title']}* by {s['artist']}\n"
        return result_str
    else:
        return "❌ Song not found. Try typing 'list' to see all songs."

def send_whatsapp_message(to_number, message_text):
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("Missing token or phone ID")
        return
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Gospel Bot LIVE", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification token mismatch", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        if data.get("object"):
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        message = messages[0]
                        from_number = message.get("from")
                        msg_body = message.get("text", {}).get("body", "")
                        if msg_body:
                            reply_text = search_songs(msg_body)
                            send_whatsapp_message(from_number, reply_text)
            return "EVENT_RECEIVED", 200
    except Exception as e:
        print(f"Error: {e}")
    return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
