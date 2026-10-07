"""Repeatable checks of the game's real ladder decisions and basic movement.

Run with: python check_barrel_descent.py
No display or additional test dependencies are needed.
"""

import random
import unittest
from collections import defaultdict
from unittest.mock import patch

import pygame

from game import BARREL_R, BARREL_SPEED, LADDERS, PLATFORMS, Barrel, Player, platform_y


def approaching_barrel(index, dt=1 / 60):
    lx, _, upper = LADDERS[index]
    barrel = Barrel()
    barrel.plat = upper
    slope = PLATFORMS[upper][3] - PLATFORMS[upper][2]
    barrel.direction = -1 if slope < 0 else 1
    barrel.pos.x = lx - barrel.direction * BARREL_SPEED * dt
    return barrel


class BarrelDescentChecks(unittest.TestCase):
    def test_probability_boundary_at_every_ladder(self):
        for index in range(len(LADDERS)):
            for value in (0.0, 0.299999, 0.3, 0.300001, 0.699999, 0.7, 0.999999):
                with self.subTest(ladder=index, random=value):
                    barrel = approaching_barrel(index)
                    with patch('game.random.random', return_value=value) as draw:
                        barrel.update(1 / 60)
                    self.assertEqual(barrel.ladder, index if value < 0.3 else None)
                    self.assertEqual(draw.call_count, 1)
                    self.assertIn(index, barrel.skip)

    def test_rejected_ladder_is_not_retried(self):
        barrel = approaching_barrel(3)
        with patch('game.random.random', side_effect=(0.3, 0.0)) as draw:
            barrel.update(1 / 60)
            barrel.update(1 / 60)  # Still inside the three-pixel encounter range.
            barrel.pos.x = LADDERS[3][0]  # Revisiting must also preserve the decision.
            barrel.update(0)
        self.assertIsNone(barrel.ladder)
        self.assertEqual(draw.call_count, 1)

    def test_accepted_ladder_does_not_reroll(self):
        barrel = approaching_barrel(3)
        with patch('game.random.random', return_value=0.0) as draw:
            barrel.update(1 / 60)
            for _ in range(10):
                barrel.update(1 / 60)
        self.assertEqual(barrel.ladder, 3)
        self.assertEqual(draw.call_count, 1)

    def test_ineligible_encounters_do_not_draw(self):
        for wrong_platform, offset in ((True, 0), (False, 3), (False, -3), (False, 20)):
            barrel = approaching_barrel(3, dt=0)
            barrel.pos.x += offset
            if wrong_platform:
                barrel.plat = 0
            with patch('game.random.random') as draw:
                barrel.update(0)
            draw.assert_not_called()
            self.assertEqual(barrel.skip, set())

    def test_seeded_sample_uses_actual_barrel_update(self):
        generator = random.Random(579)
        trials = 10000
        descents = 0
        with patch('game.random.random', side_effect=generator.random) as draw:
            for encounter in range(trials):
                barrel = approaching_barrel(encounter % len(LADDERS))
                barrel.update(1 / 60)
                descents += barrel.ladder is not None
        self.assertEqual(draw.call_count, trials)
        self.assertLess(abs(descents / trials - 0.3), 0.015)
        print(f'\nSeed 579: {descents}/{trials} eligible encounters descended ({descents / trials:.2%}).')

    def test_barrel_roll_descent_and_edge_fall(self):
        barrel = approaching_barrel(3)
        with patch('game.random.random', return_value=0.3):
            barrel.update(1 / 60)
        x = barrel.pos.x
        barrel.update(1 / 60)
        self.assertGreater(barrel.pos.x, x)
        self.assertEqual(barrel.pos.y + BARREL_R, platform_y(PLATFORMS[4], barrel.pos.x))

        barrel = approaching_barrel(3)
        with patch('game.random.random', return_value=0.0):
            barrel.update(1 / 60)
        y = barrel.pos.y
        barrel.update(1 / 60)
        self.assertGreater(barrel.pos.y, y)
        for _ in range(120):
            barrel.update(1 / 60)
            if barrel.ladder is None:
                break
        self.assertIsNone(barrel.ladder)
        self.assertEqual(barrel.plat, 3)
        barrel.update(1 / 60)
        self.assertAlmostEqual(barrel.pos.y + BARREL_R, platform_y(PLATFORMS[3], barrel.pos.x))

        barrel = Barrel()
        barrel.pos.x = PLATFORMS[4][1] - 1
        barrel.update(1 / 60)
        self.assertIsNone(barrel.plat)
        for _ in range(120):
            barrel.update(1 / 60)
            if barrel.plat is not None:
                break
        self.assertEqual(barrel.plat, 3)

    def test_player_walk_jump_climb_and_reset(self):
        player = Player()
        keys = defaultdict(int, {pygame.K_RIGHT: 1})
        player.update(1 / 60, keys)
        self.assertGreater(player.pos.x, 40)
        self.assertEqual(player.pos.y, 570)
        player.jump()
        player.update(1 / 60, defaultdict(int))
        self.assertLess(player.pos.y, 570)
        for _ in range(120):
            player.update(1 / 60, defaultdict(int))
        self.assertTrue(player.on_ground)
        self.assertEqual(player.pos.y, 570)
        player.pos.x = LADDERS[0][0]
        up = defaultdict(int, {pygame.K_UP: 1})
        player.update(1 / 60, up)
        self.assertEqual(player.ladder, 0)
        for _ in range(120):
            player.update(1 / 60, up)
            if player.ladder is None:
                break
        self.assertIsNone(player.ladder)
        self.assertAlmostEqual(player.pos.y, platform_y(PLATFORMS[1], player.pos.x))
        player.update(1 / 60, keys)
        self.assertAlmostEqual(player.pos.y, platform_y(PLATFORMS[1], player.pos.x))
        player.reset()
        self.assertEqual(tuple(player.pos), (40, 570))
        self.assertTrue(player.on_ground)
        self.assertIsNone(player.ladder)


if __name__ == '__main__':
    unittest.main(verbosity=2)
