import unittest

import config
from pyg.font import Font


class Test_Font(unittest.TestCase):
    def setUp(self):
        self.font = Font(config.menufontpath, config.menufontsize)


    def test_char_width_is_cropped_to_bounding_box(self):
        self.assertEqual(self.font.chars['A'].get_size(), (5, 8))
        self.assertEqual(self.font.chars['I'].get_size(), (3, 8))
        self.assertEqual(self.font.chars['a'].get_size(), (5, 8))


    def test_line_of_text_is_correct_width_and_height(self):
        self.assertEqual(self.font.render('AIa').get_size(), (13, 8))  # 5+3+5, 8


    def test_tracking_increases_width(self):
        self.assertEqual(self.font.render('AIa', tracking=2).get_width(), 19)  # 5+3+5 + 2*3


    def test_multiple_lines_of_text_are_width_of_longest_line(self):
        self.assertEqual(self.font.render('AIa\nAIaa\nA').get_width(), 18)  # 5+3+5+5


    def test_multiple_lines_of_text_are_correct_height(self):
        self.assertEqual(self.font.render('A\nA\nA').get_height(), 24)  # 8*3


    def test_lineheight_increases_height(self):
        self.assertEqual(self.font.render('A\nA\nA', lineheight=10).get_height(), 30)  # 10*3


    def test_charheight_scales_height(self):
        self.assertEqual(self.font.render('A\nA\nA', charheight=13).get_height(), 39)  # 13*3


    def test_charheight_scales_width(self):
        self.assertEqual(self.font.render('AIa', charheight=16).get_width(), 26)  # 5+3+5*(16/8)


    def test_charheight_scales_tracking(self):
        self.assertEqual(self.font.render('AIa', charheight=16, tracking=1).get_width(), 32)


    def test_passing_a_list_returns_a_list(self):
        line1, line2 = self.font.render(['AIa', 'AIa\nAIaa\nA'])
        self.assertEqual((line1.get_size(), line2.get_size()), ((13, 8), (18, 24)))
