"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Taste profiles
#
# Each profile is a dictionary of target values for the scoring features.
# Keys that are present are scored; keys that are absent are skipped.
#
# Critique: a profile needs at least energy + valence to separate songs that
# share the same genre/mood label. Without those two numbers, "intense rock"
# and "chill lofi" can score identically when neither matches genre/mood.
# ---------------------------------------------------------------------------

PROFILES = {
    # A focused late-night work session: low energy, calm, highly acoustic.
    # Should strongly prefer lofi/ambient over rock or EDM.
    "Late Night Study": {
        "genre":    "lofi",
        "mood":     "chill",
        "energy":   0.38,
        "valence":  0.58,
    },

    # A high-energy workout: loud, intense, electric — not acoustic at all.
    # Should strongly prefer rock/metal/EDM over lofi or classical.
    "Workout Mode": {
        "genre":    "rock",
        "mood":     "intense",
        "energy":   0.92,
        "valence":  0.45,
    },

    # A happy weekend morning: upbeat, warm, moderate energy.
    # Should prefer pop/funk/reggae; should score lofi and metal poorly.
    "Weekend Morning": {
        "genre":    "pop",
        "mood":     "happy",
        "energy":   0.75,
        "valence":  0.82,
    },
}


def run_profile(name: str, prefs: dict, songs: list, k: int = 5) -> None:
    print(f"\n{'=' * 50}")
    print(f"  Profile : {name}")
    print(f"  Wants   : genre={prefs.get('genre','?')}  mood={prefs.get('mood','?')}  "
          f"energy={prefs.get('energy','?')}  valence={prefs.get('valence','?')}")
    print(f"{'=' * 50}")

    recommendations = recommend_songs(prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}")
        print(f"       {song['artist']}  |  {song['genre']} / {song['mood']}")
        print(f"       Score: {score:.2f} / 5.50")
        for reason in explanation.split(", "):
            print(f"         • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
