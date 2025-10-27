
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, HTTPException 
from model2 import predict_next_song, df
import pandas as pd
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
uri = "mongodb+srv://nandini_a:test123A456@cluster0.xdjalu6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["music_db"]
songs_collection = db["songs"]

def song_serializer(song) -> dict:
    """Convert MongoDB ObjectId to string"""
    return {
        
        "Artist": song["Artist"],
        "Genre": song["Genre"],
        
    }

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/songs")
def get_songs():
    songs = list(songs_collection.find())
    return [song_serializer(song) for song in songs]

def song_serializer(song):
    return {
        "artist": song.get("Artist", "Unknown Artist"),
        "genre": song.get("Genre", "Unknown Genre"),
    }

@app.get("/songs")
def get_songs():
    try:

        songs = list(songs_collection.find())

        if not songs:
            raise HTTPException(status_code=404, detail="No songs found in database")

        return [song_serializer(song) for song in songs]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving songs: {str(e)}")

@app.get("/recommendations/mood/{mood}")
def get_mood_recommendations(mood: str):
    """Get song recommendations based on mood"""
    try:
        mood_lower = mood.lower()
        valid_moods = ["happy", "sad", "relaxed", "motivated", "confident", "melancholic", "energetic", "romantic", "calm"]
        
        if mood_lower not in valid_moods:
            raise HTTPException(status_code=400, detail="Invalid mood. Choose from: happy, sad, relaxed, motivated")
        
        songs = list(songs_collection.find({"Sentiment_Label": {"$regex": mood_lower, "$options": "i"}}).limit(20))
        
        if not songs:
            songs = list(songs_collection.find().limit(20))
        
        return [song_serializer(song) for song in songs]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving mood recommendations: {str(e)}")

@app.get("/recommendations/genre/{genre}")
def get_genre_recommendations(genre: str):
    """Get song recommendations based on genre with distinct artists"""
    try:
        genre_lower = genre.lower()
        valid_genres = ["pop", "rock", "funk"]

        if genre_lower not in valid_genres:
            raise HTTPException(status_code=400, detail="Invalid genre. Choose from: pop, rock, funk")

        pipeline = [
            {"$match": {"Genre": {"$regex": genre_lower, "$options": "i"}}},
            {"$group": {
                "_id": "$Artist",
                "song": {"$first": "$$ROOT"} 
            }},
            {"$replaceRoot": {"newRoot": "$song"}},
            {"$limit": 20}
        ]

        songs = list(songs_collection.aggregate(pipeline))

        if not songs:
            raise HTTPException(status_code=404, detail="No songs found for this genre")

        return [song_serializer(song) for song in songs]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving genre recommendations: {str(e)}")

# @app.get("/recommendations/artist/{artist}")
# def get_artist_recommendations(artist: str):
#     """Get song recommendations based on artist"""
#     try:
#         songs = list(songs_collection.find({"Artist": {"$regex": artist, "$options": "i"}}).limit(20))
        
#         if not songs:
#             songs = list(songs_collection.find().limit(20))
        
#         return [song_serializer(song) for song in songs]
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving artist recommendations: {str(e)}")

@app.get("/recommendations/artist/{artist}")
def get_artist_recommendations(artist: str):
    """Get song recommendations based on artist (distinct artists only)"""
    try:
        artist_lower = artist.lower()

        distinct_artists = songs_collection.distinct(
            "Artist",
            {"Artist": {"$regex": artist_lower, "$options": "i"}}
        )

        recommendations = []
        for art in distinct_artists:
            song = songs_collection.find_one({"Artist": art})
            if song:
                recommendations.append(song_serializer(song))

        if not recommendations:
            fallback_artists = songs_collection.distinct("Artist")
            for art in fallback_artists[:20]:
                song = songs_collection.find_one({"Artist": art})
                if song:
                    recommendations.append(song_serializer(song))

        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving artist recommendations: {str(e)}")


# @app.get("/recommendations/melody/{melody_type}")
# def get_melody_recommendations(melody_type: str):
#     """Get song recommendations based on melody type"""
#     try:

#         melody_mapping = {
#             "upbeat": "pop",
#             "mellow": "jazz", 
#             "energetic": "rock",
#             "smooth": "jazz",
#             "rhythmic": "pop"
#         }
        
#         genre = melody_mapping.get(melody_type.lower(), "pop")
#         songs = list(songs_collection.find({"Genre": {"$regex": genre, "$options": "i"}}).limit(20))
        
#         if not songs:
#             songs = list(songs_collection.find().limit(20))
        
#         return [song_serializer(song) for song in songs]
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving melody recommendations: {str(e)}")

@app.get("/recommendations/melody/{melody_type}")
def get_melody_recommendations(melody_type: str):
    """Get song recommendations based on melody type (distinct artists only)"""
    try:
        # Map melody to a genre
        melody_mapping = {
            "upbeat": "pop",
            "mellow": "jazz",
            "energetic": "rock",
            "smooth": "jazz",
            "rhythmic": "pop"
        }

        genre = melody_mapping.get(melody_type.lower(), "pop")

        distinct_artists = songs_collection.distinct(
            "Artist",
            {"Genre": {"$regex": genre, "$options": "i"}}
        )

        recommendations = []
        for artist in distinct_artists:
            song = songs_collection.find_one({"Artist": artist})
            if song:
                recommendations.append(song_serializer(song))

        if not recommendations:
            fallback_artists = songs_collection.distinct("Artist")
            for artist in fallback_artists[:20]:
                song = songs_collection.find_one({"Artist": artist})
                if song:
                    recommendations.append(song_serializer(song))

        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving melody recommendations: {str(e)}")


@app.get("/artists")
def get_artists():
    """Get list of unique artists"""
    try:
        artists = songs_collection.distinct("Artist")
        return [{"name": artist} for artist in artists[:50]]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving artists: {str(e)}")

@app.get("/melodies")
def get_melody_types():
    """Get list of melody types"""
    return [
        {"name": "Upbeat", "type": "upbeat"},
        {"name": "Mellow", "type": "mellow"},
        {"name": "Energetic", "type": "energetic"},
        {"name": "Smooth", "type": "smooth"},
        {"name": "Rhythmic", "type": "rhythmic"}
    ]

@app.post("/predict")
async def predict(data: dict):
    try:
        song_name = data.get("song_name")
        if not song_name:
            raise HTTPException(status_code=400, detail="Missing song_name")
        result = predict_next_song(song_name,df, next_words=5)
        print("🔍 MODEL RESULT:", result)  

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))