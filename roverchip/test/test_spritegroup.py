import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_SpriteGroup(unittest.TestCase):
    def setUp(self):
        self.level = Level(*MockDataFile([], []).get_data())

        self.player = self.level.add_sprite('Player', (0, 0))
        self.rover = self.level.add_sprite('Rover', (1, 1))
        self.crate = self.level.add_sprite('Crate', (0.1, 0.1))
        self.crate2 = self.level.add_sprite('Crate', (1.75, 1.75))

        self.sprites = self.level.sprites


    def test_flag_attribute_returns_sprites_for_which_flag_is_true(self):
        self.rover.is_active = False
        self.assertItemsEqual(self.sprites.active, [self.player, self.crate, self.crate2])


    def test_get_item_syntax_returns_sprites_with_certain_type(self):
        self.assertItemsEqual(self.sprites['Crate'], [self.crate, self.crate2])
        self.assertItemsEqual(self.sprites['Rover', 'Player'], [self.rover, self.player])


    def test_get_item_syntax_doesnt_filter_if_passed_none(self):
        self.assertItemsEqual(self.sprites[None], self.sprites)


    def test_methods_can_be_chained(self):
        self.rover.is_active = False
        self.assertItemsEqual(self.sprites['Player', 'Rover'].active, [self.player])
        self.assertItemsEqual(self.sprites.active['Player', 'Rover'], [self.player])


    def test_at_method_filters_sprites_by_position(self):
        self.assertItemsEqual(self.sprites.at((1, 1)), [self.rover])


    def test_at_method_filters_by_multiple_positions(self):
        self.assertItemsEqual(self.sprites.at((0, 0), (1.75, 1.75)), [self.player, self.crate2])


    def test_on_method_filters_sprites_by_overlapping_position(self):
        self.assertItemsEqual(self.sprites.on((1, 1)), [self.rover, self.crate, self.crate2])


    def test_on_method_filters_by_multiple_positions(self):
        self.assertItemsEqual(self.sprites.on((0.5, -0.5), (0.5, 1.5)),
                              [self.player, self.crate, self.rover])