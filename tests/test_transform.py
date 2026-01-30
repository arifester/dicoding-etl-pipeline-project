import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_data_success(self):
        # Input: Raw dirty data
        raw_data = [{
            "Title": "Test Shirt",
            "Price": "$100.00",
            "Rating": "Rating: 4.5 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "Timestamp": "2024-01-01"
        }]

        df = transform_data(raw_data)

        # Assertions
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]['Price'], 1600000.0) # 100 * 16000
        self.assertEqual(df.iloc[0]['Rating'], 4.5)
        self.assertEqual(df.iloc[0]['Colors'], 3)
        self.assertEqual(df.iloc[0]['Size'], "M")
        self.assertEqual(df.iloc[0]['Gender'], "Men")

    def test_transform_data_empty(self):
        # Test with empty input
        df = transform_data([])
        self.assertTrue(df.empty)

    def test_transform_invalid_data(self):
        # Input: Contains "Unknown Product" and "Price Unavailable"
        raw_data = [
            {"Title": "Unknown Product", "Price": "$10.00", "Rating": "", "Colors": "", "Size": "", "Gender": "", "Timestamp": ""},
            {"Title": "Valid Product", "Price": "Price Unavailable", "Rating": "", "Colors": "", "Size": "", "Gender": "", "Timestamp": ""}
        ]
        
        df = transform_data(raw_data)
        
        # Should be empty because both rows are invalid based on logic
        self.assertTrue(df.empty)

if __name__ == '__main__':
    unittest.main()
