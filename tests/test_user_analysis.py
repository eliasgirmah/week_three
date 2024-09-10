import sys
import os

# Add the parent directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# tests/test_user_analysis.py

import unittest
from src.user_analysis import get_top_10_handsets, aggregate_user_data

class TestUserAnalysis(unittest.TestCase):
    def test_get_top_10_handsets(self):
        df = get_top_10_handsets()
        self.assertIsNotNone(df, "DataFrame should not be None")
        self.assertTrue(len(df) <= 10, "The result should have at most 10 entries")

    def test_aggregate_user_data(self):
        df = aggregate_user_data()
        self.assertIsNotNone(df, "DataFrame should not be None")
        self.assertTrue("user_id" in df.columns, "The result should contain 'user_id'")

if __name__ == "__main__":
    unittest.main()
