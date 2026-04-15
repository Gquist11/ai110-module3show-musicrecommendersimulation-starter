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

# ---------------------------------------------------------------------------
# Edge-case / adversarial profiles
#
# These are designed to stress-test the scoring logic by exposing known
# weaknesses: conflicting categorical vs. numeric signals, labels that don't
# exist in the catalog, and profiles with no categorical preferences at all.
# ---------------------------------------------------------------------------

EDGE_CASE_PROFILES = {
    # Conflict: sad mood lives in low-energy blues songs (energy ~0.35),
    # but this profile demands high energy (0.9). Genre + mood will fire for
    # "3 AM Blues" (+3.5 pts) but its energy penalty (-0.55) is severe.
    # High-energy songs score well on energy but earn zero label points.
    # Expected: "3 AM Blues" still wins on label weight alone — exposing that
    # genre+mood can override a very bad energy match.
    "High-Energy Sad": {
        "genre":    "blues",
        "mood":     "sad",
        "energy":   0.90,
        "valence":  0.20,
    },

    # Ghost label: "euphoric" does not exist in the catalog, so the mood
    # bonus (+1.5) can never fire for any song. The genre bonus for "pop"
    # still fires, but the max reachable score drops from 5.5 to 4.0.
    # Expected: pop songs rise to the top on genre alone; mood is useless.
    "Ghost Mood": {
        "genre":    "pop",
        "mood":     "euphoric",
        "energy":   0.80,
        "valence":  0.90,
    },

    # Numeric only: no genre or mood keys at all — only continuous targets.
    # The maximum reachable score drops to 1.5 (energy 1.0 + valence 0.5).
    # Expected: all songs cluster tightly in score; the ranking becomes
    # much less decisive and nearly any mid-energy song can reach the top.
    "Numbers Only": {
        "energy":   0.50,
        "valence":  0.50,
    },

    # Impossible combo: "metal" is the genre but "happy" is the mood.
    # Iron Curtain is the only metal song and its mood is "angry," not "happy."
    # No song in the catalog is both metal AND happy, so genre and mood
    # bonuses can never fire at the same time.
    # Expected: Iron Curtain wins on genre alone; happy songs score mood
    # points but miss on genre — a split that reveals the all-or-nothing bias.
    "Metal + Happy": {
        "genre":    "metal",
        "mood":     "happy",
        "energy":   0.95,
        "valence":  0.80,
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
        print(f"       Score: {score:.2f} / 5.00")
        for reason in explanation.split(", "):
            print(f"         • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    print("\n\n*** STANDARD PROFILES ***")
    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs)

    print("\n\n*** EDGE CASE / ADVERSARIAL PROFILES ***")
    for name, prefs in EDGE_CASE_PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
