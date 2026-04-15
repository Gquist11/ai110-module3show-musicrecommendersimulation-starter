# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder recommends songs from a small catalog based on what a user is in the mood for right now. It is designed for a single listener who can describe their current vibe using a genre, a mood, and an energy level.

- It generates ranked song recommendations from a 10-song catalog
- It assumes the user knows roughly what they want (e.g. "I want pop, happy, high energy")
- This is a classroom simulation, not a production system — the catalog is intentionally small to make the logic easy to inspect and reason about

---

## 3. How the Model Works

The recommender works in two steps: scoring and ranking.

**Scoring Rule — how one song gets a number:**

Every song is compared to the user's preferences across four features. Each feature contributes a certain number of points toward a total score between 0 and 1:

- **Genre match (30 points):** If the song's genre exactly matches what the user wants, it gets the full 30 points. Otherwise it gets zero. Genre is worth the most because it is the broadest filter — a jazz fan rarely wants metal no matter how good the energy match is.
- **Mood match (25 points):** Same idea — full points for an exact match, zero otherwise. Mood reflects *why* you are listening right now, which makes it the second most important signal.
- **Energy closeness (25 points):** Unlike genre and mood, energy is a number between 0 and 1. Instead of rewarding high or low energy, the system rewards *closeness* to the user's target. A song that is 0.02 away from the target scores nearly full points; a song that is 0.50 away scores much less. The formula is: `points = 25 × (1 − difference)`.
- **Valence closeness (20 points):** Valence measures musical positivity. It uses the same closeness formula as energy. It is weighted slightly less because it is a finer-grained signal that most listeners do not consciously think about.

**Ranking Rule — how the list is built:**

Once every song has a score, the system sorts all songs from highest to lowest and returns the top 5. This is the ranking step. It is separate from scoring because scoring judges each song on its own, while ranking compares them all against each other and picks the winners.

---

## 4. Data

- The catalog contains **10 songs**
- Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop
- Moods represented: happy, chill, intense, relaxed, focused, moody
- No data was added or removed from the starter dataset
- Missing from the dataset: classical, hip-hop, R&B, country, and electronic dance music — so listeners with those tastes will get poor recommendations. There is also no information about tempo preference in the user profile, song lyrics, or listening history.

---

## 5. Strengths

- Works well for users with a clear, common vibe — a "happy pop, high energy" listener will reliably get the two pop/happy songs ranked at the top
- The energy closeness formula correctly avoids the trap of always recommending the loudest or most intense songs
- Genre acting as the top-weighted feature prevents jarring genre mismatches even when mood and energy are close
- The explanation output tells the user *why* each song was recommended, making the system transparent

---

## 6. Limitations and Bias

- **Only 10 songs** — the catalog is too small for meaningful diversity; top results often include songs the user would not actually enjoy just because there are few alternatives
- **No tempo preference** — two songs can have identical genre, mood, and energy but very different tempos (60 BPM vs 152 BPM), and the system cannot distinguish them
- **No artist diversity** — the ranking rule does not prevent the same artist from appearing multiple times in the top 5
- **Categorical matching is all-or-nothing** — a "lofi" fan gets zero genre points for an "ambient" song even though the two are very similar in practice
- **Underrepresented moods** — only one song is tagged "focused" and one is "moody", so users preferring those moods have very limited options
- **No listening history** — the system recommends the same songs every time regardless of what the user has already heard

---

## 7. Evaluation

Three user profiles were used to reason through the system's behavior:

1. `{"genre": "pop", "mood": "happy", "energy": 0.8}` — the starter profile. Expected top results: *Sunrise City* and *Rooftop Lights*, both pop/happy with high energy. This matched intuition.
2. A chill lofi listener with low energy (0.4) — expected *Midnight Coding* and *Library Rain* to dominate. The energy closeness formula correctly ranked them above louder songs.
3. An intense rock listener with energy 0.9 — *Storm Runner* should score highest. Genre and mood exact-match plus near-perfect energy proximity confirms this.

What was surprising: *Gym Hero* (pop, intense, energy 0.93) scores reasonably well for a "happy pop" user even though its mood does not match, purely because the genre and energy are strong. This shows the system can surface unexpected but plausible results.

---

## 8. Future Work

- **Add more songs** — a catalog of at least 50–100 songs would make the ranking step more meaningful
- **Soft genre matching** — group similar genres (lofi, ambient, jazz → "calm") so related genres still earn partial points
- **Tempo preference** — add `target_bpm` to the user profile and score tempo closeness the same way energy is scored
- **Diversity rule** — modify the ranking step to ensure no more than 2 songs from the same artist appear in the top 5
- **User feedback loop** — let users rate recommendations so weights can be adjusted over time instead of being hardcoded

---

## 9. Personal Reflection

Building this recommender made it clear that recommendation is really two separate problems: judging quality (the scoring rule) and making choices (the ranking rule). You cannot skip either step.

The most interesting design decision was the weight assignment. Choosing whether genre or mood should matter more forced a real question: are people more loyal to a sound or to a feeling? The answer probably depends on the person — which points to the deeper limitation of any system with fixed weights.

This project also highlighted how much information is missing from even a well-structured dataset. Features like tempo, lyrics, and listening context exist outside the spreadsheet but heavily influence what someone actually wants to hear.
