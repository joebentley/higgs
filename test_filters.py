import unittest
import random

import parse
from event import Event
from fourmomentum import FourMomentum

class TestFilteringFunctions(unittest.TestCase):

    def setUp(self):
        # Generate some events to test with
        self.events = []
        for n in range(10):
            self.events.append(Event())
            for i in range(n):
                self.events[n].momenta.append(FourMomentum([i*10,i*10,i*10],i*10))

    def test_number_filter(self):
        filtered = parse.number_threshold(self.events, 5)
        self.assertEqual(len(filtered), 4)

    def test_transverse_filter(self):
        filtered = parse.transverse_threshold(self.events, 15)
        self.assertEqual(len(filtered), 7)
        filtered = parse.transverse_threshold(self.events, 10)
        self.assertEqual(len(filtered), 8)

    def test_transverse_filter2(self):
        filtered = parse.transverse_threshold_2(self.events, 15)
        self.assertEqual(len(filtered), 7)
        self.assertEqual(len(filtered[0].momenta), 3)

    def test_energy_filter(self):
        filtered = parse.energy_threshold(self.events, 20)
        self.assertEqual(len(filtered), 6)

    def test_energy_filter2(self):
        filtered = parse.energy_threshold_2(self.events, 20)
        self.assertEqual(len(filtered), 6)
        self.assertEqual(len(filtered[0].momenta), 4)

    def test_azimuthal_filter(self):
        filtered = parse.dazi_threshold(self.events, 0.5)
        self.assertEqual(len(filtered), 8)

    def test_pseudorapidity_filter(self):
        filtered = parse.deta_threshold(self.events, 0.5)
        self.assertEqual(len(filtered), 8)

    def test_invmass_threshold(self):
        filtered = parse.invmass_threshold(self.events, 15)
        self.assertEqual(len(filtered), 7)
        filtered = parse.invmass_threshold(self.events, 45)
        self.assertEqual(len(filtered), 6)

    def test_invmass_limit(self):
        filtered = parse.invmass_limit(self.events, 15)
        self.assertEqual(len(filtered), 3)
        filtered = parse.invmass_limit(self.events, 45)
        self.assertEqual(len(filtered), 4)

    def test_highest_pt(self):
        self.events[5].filter_highest_pt(4)
        self.assertEqual(len(self.events[5].momenta), 4)


if __name__ == '__main__':
    unittest.main()
