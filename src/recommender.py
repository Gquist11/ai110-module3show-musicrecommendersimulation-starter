import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    instrumentalness: float
    speechiness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the song catalog for later scoring and ranking."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top k results."""
        def score(song: Song) -> float:
            total = 0.0
            if song.genre == user.favorite_genre:
                total += 2.0
            if song.mood == user.favorite_mood:
                total += 1.5
            total += 1.0 * (1 - abs(user.target_energy - song.energy))
            if user.likes_acoustic:
                total += 0.5 * song.acousticness
            else:
                total += 0.5 * (1 - song.acousticness)
            return total

        return sorted(self.songs, key=score, reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-English string describing why this song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"matches your preferred genre ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"matches your preferred mood ({song.mood})")
        if abs(user.target_energy - song.energy) <= 0.15:
            reasons.append(f"energy {song.energy:.2f} is close to your target {user.target_energy:.2f}")
        if user.likes_acoustic and song.acousticness >= 0.7:
            reasons.append(f"highly acoustic ({song.acousticness:.2f})")
        elif not user.likes_acoustic and song.acousticness <= 0.3:
            reasons.append(f"not acoustic ({song.acousticness:.2f})")
        return ", ".join(reasons) if reasons else "general match"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            row['instrumentalness'] = float(row['instrumentalness'])
            row['speechiness'] = float(row['speechiness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using a points-based recipe.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe (max 5.5 points):
      +2.0  genre match        (exact)
      +1.5  mood match         (exact)
      +1.0  energy similarity  (1.0 x (1 - |user - song|))
      +0.5  valence similarity (0.5 x (1 - |user - song|))

    Why this order:
      Genre ranks highest because listeners almost never cross genre boundaries
      regardless of other matches (a jazz fan rarely wants metal at any energy).
      Mood outranks energy because the same energy level means different things
      across genres. Energy and valence are continuous so they reward closeness
      rather than exact hits.
    """
    score = 0.0
    reasons = []

    if user_prefs.get('genre') and song['genre'] == user_prefs['genre']:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    if user_prefs.get('mood') and song['mood'] == user_prefs['mood']:
        score += 1.5
        reasons.append(f"mood match ({song['mood']}) +1.5")

    if user_prefs.get('energy') is not None:
        proximity = 1 - abs(user_prefs['energy'] - song['energy'])
        points = round(1.0 * proximity, 2)
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} +{points}")

    if user_prefs.get('valence') is not None:
        proximity = 1 - abs(user_prefs['valence'] - song['valence'])
        points = round(0.5 * proximity, 2)
        score += points
        reasons.append(f"valence {song['valence']:.2f} vs target {user_prefs['valence']:.2f} +{points}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "general match"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
