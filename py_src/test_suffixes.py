from unittest import TestCase

from py_src.suffixes import best_suffix


class Test(TestCase):
    def test_best_suffix(self):
        self.assertEqual(
            best_suffix(['Science Friction', 'Statue Of Liberty', 'This Is Pop?', 'Are You Receiving Me?', 'Life Begins At The Hop', 'Making Plans For Nigel', 'Ten Feet Tall', 'Wait Till Your Boat Goes Down', 'Generals And Majors (Edit)', 'Towers Of London (Edit)', 'Sgt. Rock (Is Going To Help Me)', 'Love At First Sight', 'Respectable Street', 'Senses Working Overtime', 'Ball And Chain', 'No Thugs In Our House', 'Great Fire', 'Wonderland', "Love On A Farmboy's Wages", 'All You Pretty Girls', 'This World Over (Edit)', 'Wake Up (Edit)', 'Grass (Edit)', 'The Meeting Place', 'Dear God', 'Mayor Of Simpleton', 'King For A Day', 'The Loving', 'The Disappointed', 'Ballad Of Peter Pumpkinhead', 'Wrapped In Grey']),
            ' (Edit)'
        )
