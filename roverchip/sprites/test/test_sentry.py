import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Player(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0, 1],
                 [0, 2, 0, 0]]
        ctypes = [('Floor',), ('Wall',), ('SentryButton',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 1))
        self.sentry = self.level.add_sprite('Sentry', (0, 0), 3)

        # time to move 1 cell
        self.playertime = 1000 / self.player.speed
        self.sentrytime = 1000 / self.sentry.speed


    def test_sentry_turns_when_button_triggered(self):
        self.player.attempt_move(1)
        self.level.update_level(self.playertime)
        self.assertEqual(self.sentry.rotate, 1)


    def test_sentry_moves_forward_when_possible(self):
        self.sentry.rotate = 1
        self.level.update_level(self.sentrytime)
        self.assertEqual(self.sentry.pos, (1, 0))
        self.level.update_level(self.sentrytime)
        self.assertEqual(self.sentry.pos, (2, 0))
        self.level.update_level(self.sentrytime)
        self.assertEqual(self.sentry.pos, (2, 0)) # stopped by wall
