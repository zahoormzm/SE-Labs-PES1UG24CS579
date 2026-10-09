# Software Engineering Lab 4 - Donkey Kong Repair

**SRN:** PES1UG24CS579

**Assigned repository:** [SETAPESU26/30_donkeykong](https://github.com/SETAPESU26/30_donkeykong)

**Personal repository:** SE-Labs-PES1UG24CS579

All assignment changes are inside `Lab-4`. Earlier labs and the original
assigned repository are preserved. Submission updates go only to the personal
repository, `zahoormzm/SE-Labs-PES1UG24CS579`, on `main`; no pull request is created.

## Setup and play

Python 3.12 was used for verification. From this repository's `Lab-4` folder,
run the already prepared environment:

```bash
/Users/zahoormashahir/Documents/ChatGPT/SE/work/lab4-venv/bin/python game.py
```

On another computer with Python 3.12 installed:

```bash
cd Lab-4
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python game.py
```

The only game dependency is Pygame 2.6.1, pinned in `requirements.txt`.
Left/Right move, Space jumps, Up/Down climb nearby ladders, and R restarts.
Reach the princess to win; barrel collisions cost lives.

## Completed tasks

| Task | Implementation |
| --- | --- |
| 1. Ladder descent | Changed `random.random() < 0.7` to `< 0.3`. Each eligible encounter has about a 30% descent chance. The existing skip set preserves one decision per ladder for each barrel. |
| 2. Background | Navy `(15, 15, 25)` below 500 points, dark purple `(35, 20, 50)` at 500-999, warm dark brown `(50, 25, 20)` at 1000 or above. |
| 3. Jump effect | One yellow floating points label per cleared barrel. It rises for about one second and displays the exact integer bonus stored on that barrel. The original callback interface is retained. |
| 4. Multiplier | 1x below 1000 points; 2x at 1000 or above, calculated from the score before adding the jump bonus. The HUD displays the multiplier for the next jump. |

A jump from 900 to 1000 awards **+100** and changes the HUD to **2x**.
The next successful jump awards **+200**. The background changes immediately
with the new score. The floating label always shows the bonus just awarded.

R resets the player, score, lives, game state, barrels, temporary labels, and
the initial one-second spawn delay. Navy and 1x are restored. Temporary labels
also clear on life loss and on starting a fresh game.

## Verification

From `Lab-4`, run:

```bash
/Users/zahoormashahir/Documents/ChatGPT/SE/work/lab4-venv/bin/python -m unittest -v check_features check_barrel_descent
```

All **10 checks passed** on 7 October 2026 and again on 9 October 2026:

- Controlled random values at all four ladders: below 0.3 descends; exactly
  0.3 and above keeps rolling. Repeated frames and revisits do not reroll.
- Seed 579, 10,000 actual barrel encounters: 2,988 descents (**29.88%**).
- Barrel rolling, ladder descent, edge falling/landing, and player movement.
- Background thresholds 499/500 and 999/1000; multiplier threshold 999/1000.
- Actual main-loop scoring from 900 to 1000 and then to 1200, exact labels,
  HUD multiplier, one callback per cleared barrel, and complete R cleanup.
- Labels rise 15 pixels in half a second, expire at one second, and remain
  anchored to the jump location rather than following the barrel.

Earlier controlled runs of the real game and display also checked walking,
climbing, jumping/landing, reset, rendering, and floating labels. Controlled
tests are verification only and are not presented as submission gameplay.

## Deliverables and current status

| Deliverable | Location / status |
| --- | --- |
| Updated game | [game.py](game.py) - all four tasks complete |
| Before video | [videos/PES1UG24CS579_before.mp4](videos/PES1UG24CS579_before.mp4) - exactly 14.000 seconds, source segment 00:04-00:18, as explicitly confirmed by the student |
| After video | [videos/PES1UG24CS579_after.mp4](videos/PES1UG24CS579_after.mp4) - full supplied recording, 18.633 seconds |
| Actual chat-history PDF | [chat/PES1UG24CS579_Lab4_Chat_History.pdf](chat/PES1UG24CS579_Lab4_Chat_History.pdf) - four pages, 20 actual messages covering the three assignment prompts and ending with the final response to Task 4 |

The before clip comes from `Screen Recording 2026-10-07 at 11.01.30 AM.mov`.
The student explicitly chose 00:04-00:18 (14 seconds), despite the original
assignment asking for ten seconds. It shows active gameplay and ladder descents.
It replaces the previously selected before clip.

The after clip comes from `Screen Recording 2026-10-09 at 9.38.53 AM.mov`.
Its full duration is retained. It shows active movement, barrels, reaching the
princess, the win message, and the score changing to 1000 with the warm background
and 2x HUD. It does not demonstrate the purple background stage, a floating
jump-points label, or a +200 jump award. Those behaviours passed the repeatable
checks; an additional gameplay recording would be needed to show them visually.

Both supplied recordings are genuine gameplay. Original Desktop files are
untouched. Submission copies retain the recorded audio and are encoded as
H.264/AAC MP4 at 30 fps and the original 1824 x 1480 resolution. The selected
durations are documented rather than described as ten-second clips.

The PDF is generated from the actual messages retrieved from this chat,
including the inherited earlier bug-fix and feature conversation. It contains
the three assignment prompts and their assistant conversation, ending at the
final response to the Task 4 multiplier prompt, as requested. All later
game-launch, recording, and upload discussion is excluded. The selected message
texts are preserved in order rather than invented or summarized, and every
message was checked against the generated PDF. System metadata, tool
calls/results, private reasoning, and other chat branches are excluded.
The student asked to submit the PDF only, so no shared chat URL is included.

## Final review

Reviewed the game changes against the supplied baseline on 9 October 2026.
No blocking correctness or maintainability issues were found. The ladder skip
behaviour, callback interface, pre-bonus multiplier calculation, one label per
barrel, expiry, and full R reset remain correct. All ten verification checks
passed. Both MP4s were checked for duration, readability, and gameplay content.
All actual PDF message texts were verified against the retrieved conversation,
and its pages were rendered for layout review. Only `Lab-4` changes are included.

## Submission checklist

- [x] Corrected code and all three feature functions.
- [x] Requested before gameplay segment, 00:04-00:18 (14 seconds).
- [x] Full supplied after gameplay recording (18.633 seconds), with scope noted above.
- [x] Actual chat PDF limited to the three assignment prompts through Task 4's final response; PDF only as requested.
- [x] Final code and evidence review completed before pushing the personal repo.

## Files retained for review

The submission folder contains the game, pinned dependency list, this README,
the two useful verification scripts, the actual chat PDF, and both genuine
gameplay videos. Temporary previews and export intermediates are kept outside
the submission folder. Python caches are ignored and are not deliverables.

The reviewed code and the student-selected evidence are ready to upload to the
personal repository. The original assignment's ten-second duration requirement
and the after video's feature-demonstration limitations are stated above.

## Separate implementation commits

| Commit | Change |
| --- | --- |
| `fbd1217` | Supplied Lab 4 baseline |
| `c76e135` | 30% ladder-descent fix |
| `7b45a51` | Score-based background colours |
| `9d6ef41` | Floating labels for actual jump points |
| `07dd1d0` | Threshold multiplier, HUD and complete reset |
