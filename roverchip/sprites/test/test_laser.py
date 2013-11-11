import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Laser(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
        ctypes = [('Floor',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.laser = self.level.add_sprite('Laser', (0, 1), 1)


    def test_laser_creates_laserbeams(self):
        self.level.update_level([], 1)
        self.assertItemsEqual([beam.pos for beam in self.level.sprites['Laserbeam']],
                              [(1, 1), (2, 1), (3, 1)])


    def test_solid_object_blocks_laserbeams(self):
        self.level.add_sprite('Crate', (2, 1), 2)
        self.level.update_level([], 1)
        self.assertItemsEqual([beam.pos for beam in self.level.sprites['Laserbeam']],
                              [(1, 1)])


    def test_mirror_bounces_laserbeams(self):
        self.level.add_sprite('Mirror', (2, 1), 2)
        self.level.update_level([], 1)
        self.assertItemsEqual([beam.pos for beam in self.level.sprites['Laserbeam']],
                              [(1, 1), (2, 1), (2, 2)])


    def test_laserbeam_kills_destructible_sprites(self):
        player = self.level.add_sprite('Player', (1, 1))
        rover = self.level.add_sprite('Rover', (2, 1))
        robot = self.level.add_sprite('Robot', (3, 1))
        self.level.update_level([], 1)
        self.assertNotIn(player, self.level.sprites)
        self.assertNotIn(rover, self.level.sprites)
        self.assertNotIn(robot, self.level.sprites)
