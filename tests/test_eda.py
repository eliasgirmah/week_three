import unittest
import pandas as pd
from src.eda import descriptive_statistics

class TestEDA(unittest.TestCase):
    def test_descriptive_statistics(self):
        # Sample dataframe
        data = {'TotalPremium': [100, 200, 300], 'TotalClaims': [10, 20, 30]}
        df = pd.DataFrame(data)
        
        # Run descriptive statistics
        result = descriptive_statistics(df, ['TotalPremium', 'TotalClaims'])
        
        # Check if the result is a DataFrame
        self.assertIsInstance(result, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
