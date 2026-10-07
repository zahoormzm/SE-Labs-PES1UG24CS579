# Software Engineering Lab 4 - Donkey Kong Repair

**SRN:** PES1UG24CS579

**Assigned repository:** [SETAPESU26/30_donkeykong](https://github.com/SETAPESU26/30_donkeykong)

**Personal repository:** SE-Labs-PES1UG24CS579

All assignment changes are inside `Lab-4`. Earlier labs and the original
assigned repository are preserved. No push or pull request has been made.

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

All **10 checks passed** on 7 October 2026:

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
| Before video | [videos/PES1UG24CS579_before.mp4](videos/PES1UG24CS579_before.mp4) - 10.000 seconds, genuine recorded gameplay |
| After video | Pending genuine recording; save as `videos/PES1UG24CS579_after.mp4` after duration/content verification |
| Actual chat-history PDF | [chat/PES1UG24CS579_Lab4_Chat_History.pdf](chat/PES1UG24CS579_Lab4_Chat_History.pdf) - four pages, 19 actual messages available in this chat at 07 October 2026, 12:00:03 IST; refresh after any later conversation messages |
| Shared chat link | Pending: use Share > Copy link in this chat and add the actual URL here |

The before clip is the 00:03-00:13 segment of the student's Desktop recording
`Screen Recording 2026-10-07 at 11.07.15 AM.mov`, made before the first fix.
It contains active gameplay and ladder descents. Its audio was omitted; the
original recording is untouched. The output is 300 frames at 30 fps.

The PDF is generated from the actual messages retrieved from this chat,
including the inherited earlier bug-fix and feature conversation. All three
student prompts and the available assistant messages are preserved in order,
rather than invented or summarized. The text of every message was checked
against the generated PDF. It excludes other chat branches, system metadata,
tool calls/results, and private reasoning. The cover states the snapshot time
and message count; later messages require a refreshed export.

## Record the after video

1. Run the completed `game.py` and play normally. Earn points by jumping over
   barrels; build score before recording so the ten-second clip can show the
   completed features.
2. Near 1000 points, press Shift-Command-5 on macOS. Choose Record Selected
   Portion and frame the game window. Under Options, select `Lab-4/videos`
   as the save location; use a five-second countdown if helpful.
3. Record at least ten seconds of active gameplay. Show jump labels, the
   background change, the HUD switching from 1x to 2x, and a +200 award.
   If time permits, press R to show cleanup and the navy/1x reset.
4. Stop from the menu bar. Keep the raw recording until a genuine ten-second
   segment has been checked and saved as `PES1UG24CS579_after.mp4`.

Do not substitute test scenarios, changed scores, staged screenshots, or an
animation for the after gameplay recording. A short random sample does not
by itself establish a 30% probability; the repeatable checks verify that rule.

## Submission checklist

- [x] Corrected code and all three feature functions.
- [x] Genuine ten-second before gameplay video.
- [ ] Genuine ten-second after gameplay video showing the completed features.
- [ ] Refresh the actual chat PDF after the final messages.
- [ ] Add the shared link with the complete conversation snapshot.
- [ ] Complete final code and evidence review before pushing the personal repo.

## Files retained for review

The submission folder contains the game, pinned dependency list, this README,
the two useful verification scripts, the actual chat PDF, and the genuine
before video. Temporary previews and export intermediates are kept outside
the submission folder. Python caches are ignored and are not deliverables.

The implementation is ready for final code review. The after video and shared
chat URL are still required before the full evidence package is ready for
submission. No push is performed as part of this preparation.

## Separate implementation commits

| Commit | Change |
| --- | --- |
| `fbd1217` | Supplied Lab 4 baseline |
| `c76e135` | 30% ladder-descent fix |
| `7b45a51` | Score-based background colours |
| `9d6ef41` | Floating labels for actual jump points |
| `07dd1d0` | Threshold multiplier, HUD and complete reset |
