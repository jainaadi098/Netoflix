from flask import Flask, render_template, request
from youtubesearchpython import VideosSearch

app = Flask(__name__)

# --- BACKUP DATA (Used if YouTube Search fails) ---
# This ensures your website is NEVER empty.
BACKUP_DATA = [
    {'title': 'John Wick 4', 'id': 'qEVUtrk8_B4', 'thumbnail': 'https://img.youtube.com/vi/qEVUtrk8_B4/maxresdefault.jpg'},
    {'title': 'Spider-Man 2', 'id': 'cqGjhVJWtEg', 'thumbnail': 'https://img.youtube.com/vi/cqGjhVJWtEg/maxresdefault.jpg'},
    {'title': 'Oppenheimer', 'id': 'uYPbbksJxIg', 'thumbnail': 'https://img.youtube.com/vi/uYPbbksJxIg/maxresdefault.jpg'},
    {'title': 'Mission Impossible', 'id': 'avz06PDqDbM', 'thumbnail': 'https://img.youtube.com/vi/avz06PDqDbM/maxresdefault.jpg'},
    {'title': 'Stranger Things', 'id': 'b9EkMc79ZSU', 'thumbnail': 'https://img.youtube.com/vi/b9EkMc79ZSU/maxresdefault.jpg'},
    {'title': 'Wednesday', 'id': 'Di310WS8zLk', 'thumbnail': 'https://img.youtube.com/vi/Di310WS8zLk/maxresdefault.jpg'},
    {'title': 'Code with Harry', 'id': '0HyIda5eub8', 'thumbnail': 'https://img.youtube.com/vi/0HyIda5eub8/maxresdefault.jpg'}
]



def get_youtube_data(query, limit=7):
    print(f"Searching YouTube for: {query}...")
    try:
        search = VideosSearch(query, limit=limit)
        results = search.result()['result']
        
        cleaned_data = []
        for video in results:
            cleaned_data.append({
                'title': video['title'],
                'id': video['id'],
                'thumbnail': video['thumbnails'][0]['url'] 
            })
        
        # If YouTube returns nothing, use backup
        if not cleaned_data:
            print("No results found. Using Backup Data.")
            return BACKUP_DATA
            
        print(f"Found {len(cleaned_data)} videos.")
        return cleaned_data

    except Exception as e:
        print(f"Error fetching data: {e}")
        # IF INTERNET FAILS, RETURN BACKUP DATA
        return BACKUP_DATA

# --- LOAD DATA ---
print("------------------------------------------------")
print("STARTING NETOFLIX...")

# We use simple queries to make sure we get results
movies_catalog = {
    "Trending Action": get_youtube_data("John Wick Action Scene", 7),
    "Horror Night": get_youtube_data("Best Horror Movie Trailers 2024", 7),
    "Sci-Fi & Fantasy": get_youtube_data("Avatar 2 Trailer", 7),
    "Coding": get_youtube_data("Code with Harry", 7)
}


tv_catalog = {
    "Netflix Originals": get_youtube_data("Stranger Things Trailer", 7),
    "Comedy Specials": get_youtube_data("Mr Bean Funny Clips", 7)
}

full_catalog = {**movies_catalog, **tv_catalog}
print("------------------------------------------------")

@app.route("/")
def home():
    query = request.args.get('q')
    if query:
        search_results = get_youtube_data(query, limit=10)
        return render_template("index.html", search_results=search_results, query=query)
    return render_template("index.html", catalog=full_catalog, page_name="Home")

@app.route("/movies")
def movies():
    return render_template("index.html", catalog=movies_catalog, page_name="Movies")

@app.route("/tv-shows")
def tv_shows():
    return render_template("index.html", catalog=tv_catalog, page_name="TV Shows")

if __name__ == "__main__":
    app.run(debug=True)