import unittest
import os
import pandas as pd

class TestSalesForecastingPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        cls.cleaned_path = os.path.join(cls.base_dir, "cleaned_data.csv")
        cls.forecast_path = os.path.join(cls.base_dir, "forecast_data.csv")

    def test_cleaned_dataset_integrity(self):
        """Verify cleaned retail dataset contains required sales columns."""
        self.assertTrue(os.path.exists(self.cleaned_path), "cleaned_data.csv must exist.")
        df = pd.read_csv(self.cleaned_path)
        required_cols = ['Order Date', 'Region', 'Category', 'Sales', 'Profit']
        for col in required_cols:
            self.assertIn(col, df.columns)
        self.assertGreater(len(df), 1000)

    def test_forecast_intervals_validity(self):
        """Verify upper confidence interval is strictly greater than lower interval."""
        self.assertTrue(os.path.exists(self.forecast_path), "forecast_data.csv must exist.")
        fc = pd.read_csv(self.forecast_path)
        self.assertIn('Predicted Sales', fc.columns)
        self.assertIn('Lower Confidence Interval', fc.columns)
        self.assertIn('Upper Confidence Interval', fc.columns)
        
        # Verify valid bounds
        self.assertTrue((fc['Upper Confidence Interval'] >= fc['Lower Confidence Interval']).all())

if __name__ == '__main__':
    unittest.main()
