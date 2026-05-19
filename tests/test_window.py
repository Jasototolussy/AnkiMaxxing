from unittest.mock import patch
import win32con
from window import maximize_anki, minimize_anki


def test_maximize_anki_calls_show_window():
    with patch("window.win32gui.FindWindow", return_value=12345) as mock_find, \
         patch("window.win32gui.ShowWindow") as mock_show:
        maximize_anki()
        mock_find.assert_called_once_with(None, "Anki")
        mock_show.assert_called_once_with(12345, win32con.SW_MAXIMIZE)


def test_maximize_anki_skips_if_no_window():
    with patch("window.win32gui.FindWindow", return_value=0), \
         patch("window.win32gui.ShowWindow") as mock_show:
        maximize_anki()
        mock_show.assert_not_called()


def test_minimize_anki_calls_show_window():
    with patch("window.win32gui.FindWindow", return_value=12345) as mock_find, \
         patch("window.win32gui.ShowWindow") as mock_show:
        minimize_anki()
        mock_find.assert_called_once_with(None, "Anki")
        mock_show.assert_called_once_with(12345, win32con.SW_MINIMIZE)


def test_minimize_anki_skips_if_no_window():
    with patch("window.win32gui.FindWindow", return_value=0), \
         patch("window.win32gui.ShowWindow") as mock_show:
        minimize_anki()
        mock_show.assert_not_called()
