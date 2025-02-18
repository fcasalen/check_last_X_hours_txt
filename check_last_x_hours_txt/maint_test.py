import unittest
from unittest.mock import patch
import datetime as dt
from .main import datetime_is_in_last_X_hours  # Replace `your_module` with the actual module name

class TestDatetimeIsInLast24Hours(unittest.TestCase):

    @patch('os.path.exists')
    @patch('file_handler.FileHandler.load')
    @patch('cli_pprinter.CLIPPrinter.yellow')
    def test_datetime_within_last_24_hours(self, mock_printer, mock_file_handler, mock_os_path):
        # Mock the file handler to return a datetime within 24 hours
        mock_file_handler.return_value = (dt.datetime.now(dt.UTC) - dt.timedelta(hours=23)).isoformat()
        mock_os_path.return_value = True

        result = datetime_is_in_last_X_hours("test_file.txt")
        self.assertTrue(result)
        mock_printer.assert_not_called()

    @patch('os.path.exists')
    @patch('file_handler.FileHandler.load')
    @patch('cli_pprinter.CLIPPrinter.yellow')
    def test_datetime_outside_last_24_hours(self, mock_printer, mock_file_handler, mock_os_path):
        # Mock the file handler to return a datetime older than 24 hours
        mock_file_handler.return_value = (dt.datetime.now(dt.UTC) - dt.timedelta(hours=25)).isoformat()
        mock_os_path.return_value = True

        result = datetime_is_in_last_X_hours("test_file.txt")
        self.assertFalse(result)
        mock_printer.assert_not_called()

    @patch('os.path.exists')
    @patch('file_handler.FileHandler.load')
    @patch('cli_pprinter.CLIPPrinter.yellow')
    def test_file_not_found(self, mock_printer, mock_file_handler, mock_os_path):
        # Mock the file handler to raise FileNotFoundError
        mock_file_handler.side_effect = FileNotFoundError
        mock_os_path.return_value = False

        result = datetime_is_in_last_X_hours("nonexistent_file.txt")
        self.assertFalse(result)
        mock_printer.assert_not_called()

    @patch('os.path.exists')
    @patch('file_handler.FileHandler.load')
    @patch('cli_pprinter.CLIPPrinter.yellow')
    def test_invalid_datetime_format(self, mock_printer, mock_file_handler, mock_os_path):
        # Mock the file handler to return a malformed datetime string
        mock_file_handler.return_value = "invalid-datetime"
        mock_os_path.return_value = True

        result = datetime_is_in_last_X_hours("malformed_file.txt")
        self.assertFalse(result)
        mock_printer.assert_called_once_with(
            'Error converting string to date. The string in malformed_file.txt is not in isoformat'
        )

    @patch('os.path.exists')
    @patch('file_handler.FileHandler.load')
    @patch('cli_pprinter.CLIPPrinter.yellow')
    def test_custom_hours_parameter(self, mock_printer, mock_file_handler, mock_os_path):
        # Mock the file handler to return a datetime within the last 10 hours
        mock_file_handler.return_value = (dt.datetime.now(dt.UTC) - dt.timedelta(hours=9)).isoformat()
        mock_os_path.return_value = True

        result = datetime_is_in_last_X_hours("test_file.txt", hours=10)
        self.assertTrue(result)
        mock_printer.assert_not_called()

        # Test with a datetime outside the last 10 hours
        mock_file_handler.return_value = (dt.datetime.now(dt.UTC) - dt.timedelta(hours=11)).isoformat()

        result = datetime_is_in_last_X_hours("test_file.txt", hours=10)
        self.assertFalse(result)
        mock_printer.assert_not_called()

if __name__ == '__main__':
    unittest.main()
