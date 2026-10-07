"""Check score thresholds, actual jump awards, HUD labels, and restart cleanup.

Run with: python check_features.py
The controlled main-loop test is verification, not submission gameplay footage.
"""

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import unittest
from collections import defaultdict
from unittest.mock import patch

import pygame
import game


class FeatureChecks(unittest.TestCase):
    def tearDown(self):
        game.point_labels.clear()
        pygame.quit()

    def test_score_thresholds(self):
        for score, colour, multiplier in (
            (0, game.BG, 1), (499, game.BG, 1),
            (500, (35, 20, 50), 1), (999, (35, 20, 50), 1),
            (1000, (50, 25, 20), 2), (1001, (50, 25, 20), 2),
        ):
            with self.subTest(score=score):
                self.assertEqual(game.theme_color(score), colour)
                self.assertEqual(game.score_multiplier(score), multiplier)

    def test_label_lifetime_and_position_copy(self):
        barrel = game.Barrel()
        barrel.jump_points = 200
        game.on_barrel_jumped(game.Player(), barrel)
        effect = game.point_labels[0]
        self.assertEqual(effect["points"], 200)
        self.assertLess(effect["pos"].y, barrel.pos.y - game.BARREL_R)
        initial = effect["pos"].copy()
        barrel.pos.x += 100
        self.assertEqual(effect["pos"], initial)
        game.update_point_labels(0.5)
        self.assertAlmostEqual(effect["pos"].y, initial.y - 15)
        self.assertEqual(len(game.point_labels), 1)
        game.update_point_labels(0.5)
        self.assertEqual(game.point_labels, [])

    def test_main_loop_awards_use_previous_score_and_restart(self):
        frame = 0
        snapshots = []
        hud_text = []
        barrels_created = []
        real_player, real_barrel = game.Player, game.Barrel
        real_draw, real_font = game.draw_scene, pygame.font.Font
        game.point_labels.append({"pos": pygame.Vector2(), "points": 999, "remaining": 1})

        class Clock:
            def tick(self, fps):
                return 50

        class Font:
            def __init__(self, *args):
                self.font = real_font(*args)
            def render(self, text, *args):
                if text.startswith("Score "):
                    hud_text.append(text)
                return self.font.render(text, *args)

        def player_factory():
            player = real_player()
            # Hold an airborne player above the test barrels to exercise scoring.
            player.pos.update(500, 535)
            player.on_ground = False
            return player

        def barrel_factory():
            barrel = real_barrel()
            barrel.plat = 0
            barrel.pos.update(500, 560)
            barrels_created.append(barrel)
            return barrel

        def events():
            if frame == 32:
                return [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)]
            if frame == 34:
                return [pygame.event.Event(pygame.QUIT)]
            return []

        def draw(screen, font, player, barrels, score, lives, state):
            nonlocal frame
            real_draw(screen, font, player, barrels, score, lives, state)
            snapshots.append((score, [effect["points"] for effect in game.point_labels],
                              len(barrels), tuple(player.pos), lives, state,
                              tuple(screen.get_at((400, 100)))[:3]))
            frame += 1

        with patch("game.Player", side_effect=player_factory), \
             patch.object(real_player, "update"), \
             patch("game.Barrel", side_effect=barrel_factory), \
             patch("game.pygame.time.Clock", Clock), \
             patch("game.pygame.font.Font", Font), \
             patch("game.pygame.event.get", events), \
             patch("game.pygame.key.get_pressed", return_value=defaultdict(int)), \
             patch("game.random.uniform", return_value=0), \
             patch("game.draw_scene", draw), \
             patch("game.on_barrel_jumped", wraps=game.on_barrel_jumped) as callback:
            game.main()

        self.assertEqual(snapshots[0][1], [])  # Startup clears stale effects.
        at_threshold = next(i for i, snapshot in enumerate(snapshots) if snapshot[0] == 1000)
        self.assertEqual(snapshots[at_threshold - 1][0], 900)
        self.assertEqual(snapshots[at_threshold][1][-1], 100)  # 900 -> 1000 uses 1x.
        self.assertIn("Multiplier 2x", hud_text[at_threshold])
        self.assertEqual(snapshots[at_threshold + 1][0], 1200)
        self.assertEqual(snapshots[at_threshold + 1][1][-1], 200)  # 1000 -> 1200 uses 2x.
        self.assertEqual(callback.call_count, len(barrels_created))
        self.assertTrue(all(barrel.scored for barrel in barrels_created))
        self.assertEqual([barrel.jump_points for barrel in barrels_created[:11]], [100] * 10 + [200])
        for i in range(32, 35):
            self.assertEqual(snapshots[i], (0, [], 0, (40.0, 570.0), 3, "play", game.BG))
            self.assertIn("Multiplier 1x", hud_text[i])


if __name__ == "__main__":
    unittest.main(verbosity=2)
