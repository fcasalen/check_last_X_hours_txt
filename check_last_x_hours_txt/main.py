from file_handler import FileHandler
import datetime as dt
from cli_pprinter import CLIPPrinter
import os

def datetime_is_in_last_X_hours(file_path_to_datetime: str, hours: int = 24) -> bool:
    """
    Check if a datetime stored in a file is within the last X `hours` (default is 24).

    This function reads the first value from a file (assumed to be in ISO 8601 datetime format),
    converts it to a `datetime` object, and checks if it falls within the last `hours`.

    Args:
        file_path_to_datetime (str): The file path containing the datetime string in ISO 8601 format.
        hours (int, optional): The number of hours to check against. Defaults to 24.

    Returns:
        bool: 
            - `True` if the datetime is within the last `hours`.
            - `False` if the file is not found, the datetime is not in ISO 8601 format,
              or the datetime is outside the specified time range.

    Exceptions:
        - `FileNotFoundError`: Returns `False` and assumes the file does not exist.
        - `ValueError`: If the datetime string is invalid or not in ISO 8601 format, 
          a warning is printed via `CLIPPrinter.yellow`, and `False` is returned.

    Example:
        >>> # Assuming `test_file.txt` contains "2023-10-01T12:00:00"
        >>> datetime_is_in_last_X_hours("test_file.txt")
        True
        >>> datetime_is_in_last_X_hours("nonexistent_file.txt")
        False
        >>> datetime_is_in_last_X_hours("malformed_file.txt")  # Invalid datetime format
        Error converting string to date. Check if the string in malformed_file.txt is in isoformat
        False
    """
    if not os.path.exists(file_path_to_datetime):
        return False
    try:
        last = FileHandler.load(file_path_to_datetime, load_first_value=True)
        last = dt.datetime.fromisoformat(last)
        if (dt.datetime.now(dt.UTC) - last).total_seconds() < 3600 * hours:
            return True
        return False
    except FileNotFoundError:
        return False
    except ValueError:
        CLIPPrinter.yellow(
            f'Error converting string to date. The string in {file_path_to_datetime} is not in isoformat'
        )
        return False
