# Donkey Kong Repair Lab

This project is a single-file Donkey Kong-lite clone using **Pygame**. It introduces students to sloped-platform physics, ladder climbing, and gravity using a small, readable object-oriented codebase.

---

## What's Provided

A working Donkey Kong-lite game with:

- A player-controlled climber with jumping and gravity that follows sloped platforms
- Ladders connecting each platform level that the player can climb
- Barrels that roll down sloped platforms and occasionally descend a ladder to the level below
- Lives, scoring, and a win condition for reaching the princess

It has **one deliberate bug** and **three optional features** left as empty functions. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python game.py
```

**Controls:** Left/Right to move, Space to jump, Up/Down to grab a ladder while standing near it, `R` to reset.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the ladder-descent bug

> Barrels are supposed to take a ladder down to the next platform only occasionally, so a few keep rolling across the top platform while others trickle down toward the player. In the current build, almost every barrel immediately takes the first ladder it reaches, so the lower platforms flood with barrels and the top platform empties out fast. Find the probability check that controls this in the `Barrel` class and correct it so barrels descend roughly 3 times out of 10, not roughly 7 times out of 10.

### Task 2: Implement `theme_color(score)`

> Called once per frame in `draw_scene` as `screen.fill(theme_color(score) or BG)`, where `BG` is the default navy background `(15, 15, 25)`. It receives the player's current integer score and should return an `(r, g, b)` tuple to use as the background color, or `None` to keep the default. Idea: shift toward a warmer color as the score climbs, or briefly flash a color right after a big score gain.

### Task 3: Implement `on_barrel_jumped(player, barrel)`

> Called from the main loop exactly once, on the first frame the player is airborne directly above a barrel — right after the 100-point jump bonus is awarded for that barrel. It receives the `Player` and the `Barrel` that was jumped. Its return value is ignored; it exists purely for side effects. Idea: spawn a short-lived floating "+100" label at the barrel's position, or play a sound.

### Task 4: Implement `score_multiplier(score)`

> Called right before the barrel-jump bonus is added, as `score += int(100 * (score_multiplier(score) or 1))`. It receives the score *before* the bonus is added and should return a numeric multiplier, or `None` for the default 1x. Idea: return `2` once the score passes some threshold, to reward late-game play.

---

## Expected Behavior

- The player follows the slope of each platform instead of floating above it or sinking into it
- The player can only climb a ladder while standing near that ladder's x-position, on the platform range it connects
- Barrels roll down slopes and occasionally (about 30% of the time) descend a ladder instead of continuing to roll along the platform
- Barrels never fall through platforms
- Reaching the princess ends the game with a win message; running out of lives (from barrel collisions) ends it with a game-over message

---

## Folder Structure

```
donkey_kong/
├── game.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history

---

## PES1UG24CS579 — Lab 4 progress

Assigned repository: https://github.com/SETAPESU26/30_donkeykong

All assignment changes are maintained in this personal repository's `Lab-4` folder.

### Task 1: ladder-descent probability fixed

The original `Barrel.update` checked `random.random() < 0.7`. Since that random
value is uniformly distributed from 0 (inclusive) to 1 (exclusive), this made
about 70% of eligible ladder encounters descend. The check is now
`random.random() < 0.3`, giving about a 30% chance at each eligible encounter.
Exactly `0.3` continues rolling. A finite run may vary around 30%.

The existing `self.skip.add(index)` still happens before the probability check.
Both accepted and rejected encounters are remembered, so subsequent frames or
revisits do not give that barrel another decision at the same ladder. Eligibility,
rolling, climbing, gravity, scoring, and the three feature functions are unchanged.

Verification on 7 October 2026 using the supplied Python 3.12 environment:

- All seven checks in `check_barrel_descent.py` passed.
- Controlled values at all four ladders: `0` and `0.299999` descend;
  `0.3`, `0.300001`, `0.699999`, `0.7`, and `0.999999` continue rolling.
- Accepted encounters, rejected encounters, repeated frames, and revisits keep
  one random decision per ladder; ineligible encounters make no random draw.
- Seed 579, 10,000 encounters through the actual `Barrel.update` logic:
  2,988 descents (29.88%).
- Barrel rolling, ladder descent, falling from an edge and landing, plus player
  walking, jumping, climbing, slope following, and reset passed movement checks.
- The real game loop and display ran for 661 frames (about 11 seconds) with
  controlled input. Walking, climbing, slope movement, jumping and landing,
  reset, barrel spawning, rendering, and a clean quit passed. This was a
  verification run; it does not replace the final submission video.

To repeat the decision and movement checks from `Lab-4`:

```bash
/Users/zahoormashahir/Documents/ChatGPT/SE/work/lab4-venv/bin/python check_barrel_descent.py
```

### Task 2: score-based background implemented

`theme_color(score)` returns the original navy `(15, 15, 25)` below 500 points,
dark purple `(35, 20, 50)` from 500 through 999 points, and warm dark brown
`(50, 25, 20)` from 1000 points onward. The colours keep the existing game
elements readable. Since the colour is calculated from the current score each
frame, resetting the score to zero immediately restores navy.

Verified rendered backgrounds at scores 0, 499, 500, 999, 1000, and 2500, visually
checked all three scenes, and checked the actual main-loop restart after a
1000-point win. The restart restored score zero, normal play, and navy.

### Task 3: floating jump-points label implemented

`on_barrel_jumped(player, barrel)` keeps its original two-argument interface.
The scoring code calculates the integer bonus once, stores it as
`barrel.jump_points`, adds that same amount to the score, and then calls the
callback. This lets the label show the actual award, including any future
multiplier, without calculating the bonus again.

The callback creates a yellow `+points` label above the barrel's position. It
rises at 30 pixels per second and expires after one second. The existing
`barrel.scored` flag keeps the callback to one invocation per cleared barrel.
Effects continue to expire even when play ends. Starting a fresh game, pressing
R, or losing a life clears temporary labels.

Verified in two controlled runs of the real game loop and display, using actual
player jumping and barrel movement (302 frames total):

- A successful jump awarded 100 points and created exactly one `+100` label.
- A test-only 2.5x multiplier awarded 250 points and created exactly one `+250`
  label. `score_multiplier` itself remains unimplemented for Task 4.
- The score calculation and callback each ran once despite repeated frames.
- The label rose 15 pixels over half a second and expired after 1.00 second.
- Restarting while a label was visible cleared it, reset the player and score,
  and a fresh game also discarded stale effects.
- Visually checked the displayed label and reran all seven barrel/movement
  checks; all passed. These checks do not replace the final submission video.

### Remaining work and submission evidence

- Before gameplay video: already recorded, as reported by the student; keep the
  original 10-second recording for submission. Its location has not been supplied.
- Task 4: `score_multiplier` remains empty for a subsequent prompt.
- After gameplay video: record 10 seconds after all requested changes, showing
  the corrected barrel behaviour and the completed features.
- Updated code: keep the final version in `Lab-4`.
- Chat history: export the complete conversation as a document or PDF after
  completing the assignment, and include the shared chat link required above.
