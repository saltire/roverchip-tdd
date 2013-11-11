import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_SpriteGroup(unittest.TestCase):
    def setUp(self):
        self.level = Level(MockDataFile([], []))

        self.player = self.level.add_sprite('Player', (0, 0))
        self.rover = self.level.add_sprite('Rover', (1, 1))
        self.crate = self.level.add_sprite('Crate', (0.1, 0.1))
        self.crate2 = self.level.add_sprite('Crate', (1.75, 1.75))

        self.sprites = self.level.sprites


    def test_flag_attribute_returns_sprites_for_which_flag_is_true(self):
        self.assertItemsEqual(self.sprites.solid, [self.rover, self.crate, self.crate2])


    def test_not_flag_attribute_returns_sprites_for_which_flag_is_false(self):
        self.assertItemsEqual(self.sprites.not_solid, [self.player])


    def test_get_item_syntax_returns_sprites_by_type(self):
        self.assertItemsEqual(self.sprites['Crate'], [self.crate, self.crate2])
        self.assertItemsEqual(self.sprites['Rover', 'Player'], [self.rover, self.player])


    def test_get_item_syntax_returns_sprites_by_mixin(self):
        keydoor = self.level.add_sprite('KeyDoor', (0, 0))
        chipdoor = self.level.add_sprite('ChipDoor', (0, 0))
        self.assertItemsEqual(self.sprites['Door'], [keydoor, chipdoor])


    def test_get_item_syntax_doesnt_filter_if_passed_none(self):
        self.assertItemsEqual(self.sprites[None], self.sprites)


    def test_methods_can_be_chained(self):
        self.assertItemsEqual(self.sprites['Player', 'Rover'].solid, [self.rover])
        self.assertItemsEqual(self.sprites.solid['Player', 'Rover'], [self.rover])


    def test_at_method_filters_sprites_by_position(self):
        self.assertItemsEqual(self.sprites.at((1, 1)), [self.rover])


    def test_at_method_filters_by_multiple_positions(self):
        self.assertItemsEqual(self.sprites.at((0, 0), (1.75, 1.75)), [self.player, self.crate2])


    def test_on_method_filters_sprites_by_overlapping_position(self):
        self.assertItemsEqual(self.sprites.on((1, 1)), [self.rover, self.crate, self.crate2])


    def test_on_method_filters_by_multiple_positions(self):
        self.assertItemsEqual(self.sprites.on((0.5, -0.5), (0.5, 1.5)),
                              [self.player, self.crate, self.rover])


    def test_group_returns_list_sorted_by_decreasing_priority(self):
        self.rover.priority = 2
        self.crate2.priority = -1
        self.assertEqual(self.sprites.by_priority(),
                         [self.rover, self.player, self.crate, self.crate2])


    def test_sprite_subgroup_returns_only_sprites_in_parent(self):
        subgroup = self.sprites.subset([self.player, self.rover])
        self.sprites.discard(self.rover)
        self.assertItemsEqual(subgroup, [self.player])
        self.assertNotIn(self.rover, subgroup)

