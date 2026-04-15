# Model Card: VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0**

A points-based music recommender that matches songs to a user's current vibe.

---

## 2. Goal / Task

VibeFinder tries to answer one question: *given what a user is in the mood for right now, which songs from the catalog are the best match?*

It does not predict what you will like in general. It only looks at what you say you want at this moment — a genre, a mood, an energy level, and a positivity level. It scores every song against those preferences and returns the top 5.

---

## 3. Data Used

- **Catalog size:** 20 songs, each stored as a row in `data/songs.csv`
- **Features used for scoring:** genre (text label), mood (text label), energy (0.0–1.0), valence / positivity (0.0–1.0)
- **Features collected but not scored:** tempo in BPM, danceability, acousticness, instrumentalness, speechiness
- **Genres in the catalog:** lofi, pop, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, country, edm, reggae, metal, folk, blues, funk
- **Moods in the catalog:** happy, chill, intense, focused, energetic, romantic, peaceful, nostalgic, angry, melancholic, sad, moody, relaxed

**Limits of this dataset:**
- 20 songs is very small. Most genres only have one or two songs.
- There is no listening history — the system never learns what you have already heard.
- The genre and mood labels were assigned manually, so related sounds like "lofi" and "ambient" are treated as completely different.

---

## 4. Algorithm Summary

The system works in two steps: **scoring** and **ranking**.

**Step 1 — Score every song.**
Each song gets a number based on how well it matches the user's preferences. Four features are checked:

- **Genre match (+1.0 points):** Does the song's genre label exactly match what you asked for? If yes, full point. If no, zero.
- **Mood match (+1.5 points):** Does the song's mood label exactly match yours? If yes, full points. If no, zero.
- **Energy closeness (up to +2.0 points):** How close is the song's energy to your target? A song that is very close scores nearly 2.0. A song that is far away scores much less. The formula is `2.0 × (1 − difference)`.
- **Valence closeness (up to +0.5 points):** Same idea as energy, but for musical positivity. Smaller weight because most people do not consciously think about it.

The highest possible score is **5.0 points**.

**Step 2 — Rank and return the top 5.**
Once every song has a score, they are sorted from highest to lowest. The top 5 are returned with a plain-English explanation of which features earned points.

The scoring step and ranking step are kept separate on purpose. Scoring judges each song on its own. Ranking compares them all and picks the winners. You need both steps — scoring alone gives you 20 numbers, and ranking alone has nothing to sort.

---

## 5. Observed Behavior / Biases

**What works well:**
- For a clear, common vibe like "lofi / chill / low energy," the top results feel right immediately.
- The energy formula correctly separates songs that share the same genre and mood — it does not always pick the loudest or quietest one.
- Every result comes with a plain-English reason, so you can see exactly why a song ranked where it did.

**Known biases and limitations:**

- **Genre and mood labels are all-or-nothing.** A "lofi" fan gets zero genre points for an "ambient" song, even though both feel calm and similar. There is no partial credit for closely related labels.

- **Label weight can override a bad energy match.** In testing, a profile asking for `genre=blues, mood=sad, energy=0.90` still got *3 AM Blues* (energy 0.35) as its top result. The genre + mood bonus (+2.5 pts) was bigger than the energy penalty (−1.1 pts). The system confidently recommended a slow song to someone who asked for high energy.

- **Small catalog means genre monopolizes results.** There is only one rock song in the catalog. Any profile asking for rock will see it at the top by a huge margin — not because it is the perfect match, but because it is the only option. The system does not really *choose* the best rock song; it just finds the only one.

- **Missing mood or genre silently caps the score.** If you ask for a mood that does not exist in the catalog (like "euphoric"), the mood bonus never fires. The max reachable score quietly drops from 5.0 to 3.5. The output looks normal, but the system is handicapped with no warning.

- **No tempo, no artist diversity, no history.** Two songs can have the same genre, mood, and energy but very different tempos (think 60 BPM vs 150 BPM). The system cannot tell them apart. It also never prevents the same artist from filling all 5 slots, and it recommends the same results every single time.

---

## 6. Evaluation Process

Seven user profiles were tested: three standard profiles and four adversarial edge cases.

**Standard profiles:**

| Profile | What it tested | Top result | Surprising? |
|---|---|---|---|
| Late Night Study (lofi/chill/0.38) | Normal case with multiple matching songs | Library Rain (4.93) | #1 and #2 were only 0.02 pts apart |
| Workout Mode (rock/intense/0.92) | Normal case with only one matching song | Storm Runner (4.96) | 2+ point gap to #2 — genre monopoly |
| Weekend Morning (pop/happy/0.75) | Weight sensitivity test | Sunrise City (4.85) | Gym Hero (wrong mood) ranked #2 under old weights |

The most instructive test was running Weekend Morning twice — once with original weights (genre +2.0) and once with experimental weights (genre +1.0, energy up to +2.0). The only change was two numbers in the code, but *Rooftop Lights* (right mood, right energy) moved up and *Gym Hero* (wrong mood) moved down. That swap confirmed the genre weight was too dominant for this type of listener.

**Adversarial profiles:**

| Profile | What it exposed |
|---|---|
| High-Energy Sad (blues/sad/energy=0.90) | Label bonus beats a very bad energy match |
| Ghost Mood (pop/euphoric/0.80) | Missing mood silently caps the max score |
| Numbers Only (no labels/energy=0.50) | Without labels, all scores cluster within 0.12 pts — ranking is nearly random |
| Metal + Happy (metal/happy/0.95) | No song can earn both bonuses at once — impossible combo |

---

## 7. Intended Use and Non-Intended Use

**This system is designed for:**
- Classroom exploration of how recommendation logic works
- Understanding the tradeoffs between different scoring weights
- Seeing how small dataset size and all-or-nothing labels create bias
- Practicing the idea that scoring (judging one song) and ranking (ordering many songs) are two separate problems

**This system should NOT be used for:**
- Real music discovery — the catalog is only 20 songs and will frequently return the same results
- Users who do not already know what they want — it requires explicit genre, mood, and energy preferences
- Personalization over time — it has no memory, no listening history, and no way to learn from feedback
- Any situation where a bad recommendation causes real harm — this is a simulation, not a production tool

---

## 8. Ideas for Improvement

**1. Soft genre matching**
Right now, "lofi" and "ambient" are completely different to the system even though they feel similar. A better version would group related genres (e.g., lofi + ambient + jazz = "calm" cluster) and give partial credit when the song is in a neighboring group. This would fix the all-or-nothing label problem.

**2. Per-user weight profiles**
Every user currently uses the same weights. But a "mood-first" listener and an "energy-first" listener should be scored differently. A simple fix would let the user say which feature matters most to them, and adjust the multipliers accordingly before scoring runs.

**3. A diversity rule in the ranking step**
The scoring step judges each song individually, but the ranking step could add a rule: no more than two songs from the same artist or genre in any top-5 list. This would not change the scores — it would just enforce variety when selecting the final results.

---

## 9. Personal Reflection

**What was my biggest learning moment?**

The clearest moment was when I tested a profile that wanted high-energy music but a sad mood. The system returned a slow, quiet blues song as its top pick — and gave it a high score. The math was not broken. It was doing exactly what I told it to do. I just told it the wrong thing. That was the moment I understood that "the code works" and "the output is actually good" are two different things. A system can follow its rules perfectly and still give you a bad answer.

**How did AI tools help, and when did I need to double-check them?**

AI tools were really helpful for thinking through tradeoffs. When I was deciding how much weight to give genre vs. mood, the AI helped me think through what would happen to different types of listeners depending on the choice. That saved a lot of time.

Where I had to double-check: sometimes the AI suggested adding extra code that was not needed — things like validation functions or fallback cases for situations that would never actually happen. I had to slow down and ask "do I actually need this?" a few times. The simpler version usually worked better and was easier to understand.

**What surprised me about how a simple algorithm can still "feel" like recommendations?**

I expected the output to feel like a spreadsheet, not a playlist. But when the right songs showed up at the top — quiet lofi for studying, hard rock for a workout — it actually felt like a real recommendation. The system has no idea what music sounds like. It just adds up four numbers. But those four numbers turned out to be enough to capture what most people mean by "vibe." That was genuinely surprising.

**What would I try next?**

I would try giving partial credit for similar genres instead of zero credit. Right now, "lofi" and "ambient" are treated as completely different even though they feel very similar. If I could group nearby genres together and reward songs that are close — not just exact matches — the results would feel a lot more natural, especially for listeners who do not always know the exact genre name they want.
