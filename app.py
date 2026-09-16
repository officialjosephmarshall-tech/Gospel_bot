from flask import Flask, request, render_template_string
import csv

app = Flask(__name__)

def load_songs():
    with open("songs.csv", "r", encoding="utf-8") as file:
        return list(csv.DictReader(file))

@app.route("/")
def home():
    songs = load_songs()
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gospel Bot</title>
    </head>
    <body>
        <h1>Gospel Bot is Live</h1>
        <p>Number of songs: {{ count }}</p>

        <form action="/search" method="get">
            <input type="text" name="q" placeholder="Search song title">
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    """, count=len(songs))


@app.route("/search")
def search():
    query = request.args.get("q", "").lower()
    songs = load_songs()

    results = [
        song for song in songs
        if query in song["title"].lower()
    ]

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Songs</title>
    </head>
    <body>
        <h1>Search Gospel Songs</h1>

        <form action="/search" method="get">
            <input type="text" name="q" value="{{ query }}"
                   placeholder="Enter song title">
            <button type="submit">Search</button>
        </form>

        {% if results %}
            {% for song in results %}
                <hr>
                <h2>{{ song["title"] }}</h2>
                <p><b>Artist:</b> {{ song["artist"] }}</p>
                <p><b>Type:</b> {{ song["type"] }}</p>
                <p><b>Language:</b> {{ song["language"] }}</p>

                <h3>Lyrics</h3>
                <pre>{{ song["lyrics"] }}</pre>

                {% if song["affiliate"] %}
                    <p>
                        <a href="{{ song["affiliate"] }}">
                            Listen / Buy
                        </a>
                    </p>
                {% endif %}
            {% endfor %}
        {% else %}
            <p>No songs found.</p>
        {% endif %}

        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """, results=results, query=query)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)