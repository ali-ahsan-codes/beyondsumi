import unittest
from validate_style_profile import DARK_PALETTE, DARK_RED, is_dark_red, valid_dark_palette

class DarkPalette(unittest.TestCase):
    def test_neutral_and_optional_story_red(self):
        self.assertTrue(valid_dark_palette(DARK_PALETTE))
        self.assertTrue(valid_dark_palette({**DARK_PALETTE, "dark_red": DARK_RED}))
        self.assertTrue(valid_dark_palette({**DARK_PALETTE, "dark_red": "#901820", "mist": "#aAaAaA"}))

    def test_no_warm_paper_or_colored_base(self):
        self.assertFalse(valid_dark_palette({**DARK_PALETTE, "paper": "#fffaf0"}))
        self.assertFalse(valid_dark_palette({**DARK_PALETTE, "carbon": DARK_RED}))
        self.assertFalse(valid_dark_palette({**DARK_PALETTE, "other_accent": DARK_RED}))

    def test_other_hues_bright_red_and_malformed_values_fail(self):
        for value in ("#ff0000", "#1d3b58", "#c89b3c", "#7a6070", "#201010", "#bad", None, 42):
            self.assertFalse(is_dark_red(value))
            self.assertFalse(valid_dark_palette({**DARK_PALETTE, "dark_red": value}))

if __name__ == "__main__":
    unittest.main()
