import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Environment variables
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = "gospel123"

# List of 11 gospel songs with title and artist
SONGS = [
    {"title": "Way Maker", "artist": "Sinach"},
    {"title": "Excess Love", "artist": "Mercy Chinwo"},
    {"title": "Nara", "artist": "Tim Godfrey ft. Travis Greene"},
    {"title": "I Know Who I Am", "artist": "Sinach"},
    {"title": "Bigger Than", "artist": "Nathaniel Bassey"},
    {"title": "Imela", "artist": "Nathaniel Bassey ft. Enitan Adaba"},
    {"title": "Ekwueme", "artist": "Prospa Ochimana"},
    {"title": "You Are Great", "artist": "Steve Crown"},
    {"title": "Omemma", "artist": "Sinach"},
    {"title": "Obinasom", "artist": "Mercy Chinwo"},
    {"title": "Yahweh", "artist": "Deola Adebayo"}
]

def search_songs(query):
    """Searches for songs by name/artist or returns the full list if requested."""
    query = query.strip().lower()
    
    if query == "list":
        song_list_str = "📜 **Available Gospel Songs:**\n" + "\n".join(
            [f"{i+1}. {s['title']} - {s['artist']}" for i, s in enumerate(SONGS)]
        )
        return song_list_str

    # Search by title or artist
    results = [
        s for s in SONGS 
        if query in s["title"].lower() or query in s["artist"].lower()
    ]
    
    if results:
        result_str = "🎵 **Search Results:**\n" + "\n".join(
            [f"- *{s['title']}* by {s['artist']}" for s in results]
        )
        return result_str
    else:
        return "❌ Song not found. Try typing 'list' to see all songs, or try searching for 'Way Maker' or 'Excess Love'."

def send_whatsapp_message(to_number, message_text):
    """Sends a reply message back to the user via WhatsApp Cloud API."""
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
    return response.json()

@app.route("/", methods=["GET"])
def home():
    """Home route checking if the app is alive."""
    return "Gospel Bot LIVE", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Webhook verification route for Meta/WhatsApp."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403
    return "Bad Request", 400

@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook route that receives incoming WhatsApp messages."""
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
                            # Search the song and reply
                            reply_text = search_songs(msg_body)
                            send_whatsapp_message(from_number, reply_text)
                            
            return "EVENT_RECEIVED", 200
    except Exception as e:
        print(f"Error handling webhook: {e}")
        
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0,0,0,0",port=int(os.environ.get("PORT",10000)))

