import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_csv, load_to_postgres, load_to_sheets, load_data

class TestLoad(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Title": ["Test"],
            "Price": [1000]
        })

    # --- CSV TESTS ---
    @patch('utils.load.pd.DataFrame.to_csv')
    def test_load_to_csv_success(self, mock_to_csv):
        load_to_csv(self.df, "test.csv")
        mock_to_csv.assert_called_once()

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_load_to_csv_failure(self, mock_to_csv):
        mock_to_csv.side_effect = Exception("Permission Denied")
        load_to_csv(self.df, "test.csv")

    # --- POSTGRES TESTS ---
    def test_load_to_postgres_no_url(self):
        load_to_postgres(self.df, None)

    @patch('utils.load.create_engine')
    def test_load_to_postgres_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.return_value = mock_conn
        with patch('utils.load.pd.DataFrame.to_sql') as mock_to_sql:
            load_to_postgres(self.df, "postgresql://...")
            mock_to_sql.assert_called_once()

    @patch('utils.load.create_engine')
    def test_load_to_postgres_failure(self, mock_engine):
        mock_engine.side_effect = Exception("DB Connection Error")
        load_to_postgres(self.df, "postgresql://...")

    # --- SHEETS TESTS ---
    def test_load_to_sheets_no_id(self):
        load_to_sheets(self.df, None)

    @patch('utils.load.service_account.Credentials.from_service_account_file')
    @patch('utils.load.build')
    def test_load_to_sheets_success(self, mock_build, mock_creds):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        mock_spreadsheets = mock_service.spreadsheets.return_value
        mock_values = mock_spreadsheets.values.return_value
        mock_update = mock_values.update.return_value
        mock_update.execute.return_value = {"updatedCells": 10}

        load_to_sheets(self.df, "dummy_id")
        mock_update.execute.assert_called()

    @patch('utils.load.service_account.Credentials.from_service_account_file')
    def test_load_to_sheets_failure(self, mock_creds):
        mock_creds.side_effect = Exception("API Error")
        load_to_sheets(self.df, "dummy_id")

    # --- MAIN ORCHESTRATOR TEST ---
    def test_load_data_empty(self):
        load_data(pd.DataFrame())

    @patch('utils.load.load_to_csv')
    @patch('utils.load.load_to_postgres')
    @patch('utils.load.load_to_sheets')
    def test_load_data_full(self, mock_sheets, mock_pg, mock_csv):
        load_data(self.df, db_url="db", sheet_id="sheet")
        mock_csv.assert_called_once()
        mock_pg.assert_called_once()
        mock_sheets.assert_called_once()

if __name__ == '__main__':
    unittest.main()
