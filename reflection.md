# Reflection: Profile Comparisons

This file compares pairs of user profiles side by side and explains — in plain language — what changed between them and why it makes sense.

---

## Pair 1: Late Night Study vs. Workout Mode

**Late Night Study** wants: lofi music, chill mood, low energy (0.38), moderate positivity (0.58)
**Workout Mode** wants: rock music, intense mood, very high energy (0.92), moderate positivity (0.45)

These two profiles are on opposite ends of almost every feature. Late Night Study wants quiet, calm, slow songs. Workout Mode wants loud, aggressive, fast songs. Because the scoring system rewards songs that are *close* to your energy target, a lofi song that scores near-perfect for Late Night Study (energy 0.35 ≈ target 0.38) would score terribly for Workout Mode (energy 0.35 is 0.57 away from target 0.92). The recommendations do not overlap at all: lofi songs dominate the first list, and intense high-energy songs dominate the second.

What surprised me: Workout Mode's #1 result (*Storm Runner*, rock/intense) scored 4.97 out of 5.0 — nearly flawless. But Late Night Study's top two results (*Library Rain* and *Midnight Coding*) were separated by only 0.01 points. This shows that when there are multiple songs of the same genre and mood in the catalog, the energy formula does the fine-grained sorting. When there is only one song of a genre (like rock), the system basically has no choice — it just finds the only match.

---

## Pair 2: Weekend Morning (old weights) vs. Weekend Morning (new weights)

**Weekend Morning** wants: pop music, happy mood, medium energy (0.75), high positivity (0.82)

This is the same profile run twice — once with the original weights (genre +2.0, energy up to +1.0) and once with the experimental weights (genre +1.0, energy up to +2.0).

**Old weights — top 3:**
1. Sunrise City (pop/happy) — 4.92 ✓
2. Gym Hero (pop/intense) — 3.30 ✗ wrong mood
3. Rooftop Lights (indie pop/happy) — 2.99 ✓ right mood, wrong genre

**New weights — top 3:**
1. Sunrise City (pop/happy) — 4.85 ✓
2. Rooftop Lights (indie pop/happy) — 3.98 ✓ moved up
3. Groove Machine (funk/happy) — 3.88 ✓ moved up
4. Gym Hero (pop/intense) — 3.12 ✗ moved down

The only thing that changed was the weight numbers in the code. No songs were added or removed. But that small change flipped the #2 and #3 positions in a meaningful way: *Rooftop Lights* (which has the right mood and nearly perfect energy) now ranks above *Gym Hero* (which has the wrong mood). The new weights say: "how the song *feels* energy-wise matters more than just the genre label." That is closer to how a real person chooses music for a relaxed morning.

---

## Pair 3: Ghost Mood vs. Numbers Only (adversarial)

**Ghost Mood** wants: pop music, euphoric mood (does not exist), high energy (0.80), high positivity (0.90)
**Numbers Only** wants: no genre, no mood — just medium energy (0.50) and medium positivity (0.50)

Both of these profiles are broken in different ways. Ghost Mood has a mood label that will never match any song, so the +1.5 mood bonus can never fire. Numbers Only has no labels at all, so neither the +1.0 genre bonus nor the +1.5 mood bonus can ever fire.

The result: Ghost Mood's top songs scored around 3.3–3.5 out of 5.0. Numbers Only's top songs scored around 1.3–1.4 out of 5.0. Both lists look like normal recommendations — songs with titles and scores and reasons — but neither list is trustworthy. Ghost Mood is quietly capped because one label is missing. Numbers Only is almost completely random because the scores are so close together (top to bottom: 0.12 point spread) that the ranking means almost nothing.

What this taught me: a recommender can *look* like it is working even when it is mostly guessing. The scores seem reasonable until you notice how compressed they are. A real system would need to warn the user when their preferences are too sparse to produce meaningful results.

---

## Pair 4: High-Energy Sad vs. Metal + Happy (adversarial)

**High-Energy Sad** wants: blues/sad music at high energy (0.90) — a contradiction
**Metal + Happy** wants: metal/happy music at high energy (0.95) — a genre+mood combo that does not exist in the catalog

Both profiles ask for something the catalog cannot deliver. But they fail in different ways.

*High-Energy Sad* fails because **conflicting preferences cancel each other out unevenly**. The label bonuses (genre + mood = +2.5 pts) are large enough to pull *3 AM Blues* to the top even though its energy (0.35) is almost the worst possible match for a user who wants 0.90. The system confidently recommends a slow, quiet song to someone asking for high energy — and the math says it is "correct" to do so. The mood label wins.

*Metal + Happy* fails because **an impossible combination splits the results**. There is no metal/happy song, so the genre and mood bonuses can never fire for the same song at the same time. The top 5 ends up as a mix: one metal song that wins on genre, and several happy songs that win on mood. Nobody wins on both. The score ceiling effectively drops because the two biggest bonuses are mutually exclusive.

The difference: High-Energy Sad produces a confidently wrong answer. Metal + Happy produces an honestly uncertain answer. Both are failures, but the first one is more dangerous because it does not look like a failure.

---

## Why Does Gym Hero Keep Showing Up for "Happy Pop" Listeners?

Imagine you are at a music store asking the clerk for something "pop and happy." The clerk has a simple rule: if a song is pop, it gets 2 gold stars; if it is happy, it gets 1.5 gold stars; if the energy level is close to yours, it gets up to 2 silver stars.

*Gym Hero* is a pop song — so it gets 2 gold stars right away. But its mood is "intense," not "happy," so it gets 0 gold stars for mood. Its energy is 0.93, which is a bit high for a relaxed morning (your target is 0.75), so it earns about 1.6 silver stars on energy.

Total: 2 + 0 + 1.6 = 3.6 stars.

*Rooftop Lights* is an indie pop song — the genre does not match "pop" exactly, so it gets 0 gold stars for genre. But it *is* happy — 1.5 gold stars. And its energy (0.76) is almost exactly what you wanted — nearly 2 silver stars.

Total: 0 + 1.5 + 2.0 = 3.5 stars.

*Gym Hero* wins by 0.1 stars — purely because the clerk's rule says "pop label = 2 gold stars" and that one label is worth more than being in the wrong mood. The clerk is following the rule perfectly. The rule is just slightly wrong for this situation.

This is the core tension in any recommender: the labels are blunt categories, but music is a spectrum. A song called "pop" does not automatically belong on a happy morning playlist. Until the system can understand *context* — not just genre tags — it will keep making this kind of mistake.
