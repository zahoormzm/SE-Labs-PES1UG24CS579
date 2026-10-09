# Software Engineering Lab 4 — Donkey Kong

**SRN:** PES1UG24CS579

**Assigned repository:** [SETAPESU26/30_donkeykong](https://github.com/SETAPESU26/30_donkeykong)

## Setup

Requires Python 3.12 and Pygame 2.6.1. From the repository root:

```bash
cd Lab-4
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python game.py
```

**Controls:** Left/Right to move, Space to jump, Up/Down to climb ladders,
and R to restart. Reach the princess to win; barrel collisions cost lives.

## Completed tasks

| Task | Result |
| --- | --- |
| 1. Barrel descent | Each eligible ladder encounter has a 30% descent probability, with one decision per ladder. |
| 2. `theme_color(score)` | Navy below 500 points, dark purple at 500–999, and warm dark brown at 1000 or above. |
| 3. `on_barrel_jumped(player, barrel)` | Displays the actual jump bonus above the barrel for about one second, once per successful jump. |
| 4. `score_multiplier(score)` | Awards 1x below 1000 points and 2x at 1000 or above, using the score before the bonus. The HUD displays the current multiplier. |

A jump at 900 points awards +100; the next jump at 1000 points awards +200.
Restarting restores the initial game state, navy background, and 1x multiplier,
and clears temporary effects.

## Verification

With the virtual environment activated, run:

```bash
python -m unittest -v check_features check_barrel_descent
```

All 10 checks passed, covering ladder probability, score thresholds, jump
bonuses, floating labels, movement, and restart behaviour. The game was also
checked during gameplay.

## Submission files

| Deliverable | File |
| --- | --- |
| Updated code | [game.py](game.py) |
| Before gameplay video (14 seconds) | [PES1UG24CS579_before.mp4](videos/PES1UG24CS579_before.mp4) |
| After gameplay video (18.63 seconds) | [PES1UG24CS579_after.mp4](videos/PES1UG24CS579_after.mp4) |
| Chat history through Task 4 | [PES1UG24CS579_Lab4_Chat_History.pdf](chat/PES1UG24CS579_Lab4_Chat_History.pdf) |
