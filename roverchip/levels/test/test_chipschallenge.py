import unittest

from roverchip.levels.chipschallenge import ChipsChallenge

from roverchip.test.test_level import MockDataFile


class Test_ChipsChallenge(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 1]]
        ctypes = [('Floor',), ('Exit',)]
        self.lfile = MockDataFile(cells, ctypes)
        self.level = ChipsChallenge(self.lfile)

        self.player = self.level.add_sprite('Player', (2, 1))


    def test_level_doesnt_succeed_if_player_not_on_exit(self):
        self.player.pos = 2, 0
        self.assertFalse(self.level.check_for_success())


    def test_level_succeeds_if_no_chips_and_player_on_exit(self):
        self.assertTrue(self.level.check_for_success())


    def test_level_doesnt_succeed_if_chips_remaining(self):
        self.level.add_sprite('Chip', (1, 1))
        self.level.chipquota += 1
        self.assertFalse(self.level.check_for_success())


    def test_level_succeeds_if_chips_all_carried(self):
        chip = self.level.add_sprite('Chip', (2, 1))
        self.level.chipquota += 1
        self.player.carrying.add(chip)
        self.assertTrue(self.level.check_for_success())


    def test_chipquota_equals_property_if_passed(self):
        self.lfile.properties['chipquota'] = 2
        level = ChipsChallenge(self.lfile)
        self.assertEqual(level.chipquota, 2)


    def test_chip_quota_equals_number_of_chips_if_no_property_passed(self):
        self.lfile.spritedata = [('Chip', (0, 0)), ('Chip', (0, 1)), ('Chip', (0, 2))]
        level = ChipsChallenge(self.lfile)
        self.assertEqual(level.chipquota, 3)


    def test_level_succeeds_if_chips_carried_meets_quota(self):
        self.level.add_sprite('Chip', (0, 0))
        chip2 = self.level.add_sprite('Chip', (1, 0))
        chip3 = self.level.add_sprite('Chip', (2, 0))
        self.level.chipquota = 2
        self.assertFalse(self.level.check_for_success())
        self.player.carrying.add(chip2)
        self.assertFalse(self.level.check_for_success())
        self.player.carrying.add(chip3)
        self.assertTrue(self.level.check_for_success())


    def test_level_fails_if_player_not_active(self):
        self.assertFalse(self.level.check_for_failure())
        self.player.is_active = False
        self.assertTrue(self.level.check_for_failure())
