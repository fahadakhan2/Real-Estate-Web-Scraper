import unittest
from main import *
import re


class TestWebScraping(unittest.TestCase):

    def test_location_pattern(self):
        self.assertTrue(re.match(location_pattern, 'Winnetka_IL'))
        self.assertTrue(re.match(location_pattern, 'San-Diego_CA'))
        self.assertFalse(re.match(location_pattern, 'Winnetka_Illinois'))
        self.assertFalse(re.match(location_pattern, 'Winnetka_IL_USA'))
    
    def test_find_houses(self):
        houses = find_houses(1)
        self.assertGreaterEqual(len(houses), 0)
        for house in houses:
            self.assertGreaterEqual(house['$Price'], price_filter)
            self.assertIsNotNone(house['Address'])
            self.assertIsNotNone(house['Status'])
            self.assertIsNotNone(house['Beds'])
            self.assertIsNotNone(house['Baths'])
            self.assertIsNotNone(house['Square Feet'])
            self.assertIsNotNone(house['Acre Lot'])
            self.assertIsNotNone(house['More Info Link'])

if __name__ == '__main__':
    unittest.main()