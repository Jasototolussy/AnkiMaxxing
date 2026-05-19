from unittest.mock import patch, call
import win32con
from window import maximize_anki, minimize_anki


def _enum_found(hwnd, lst):
    lst.append(hwnd)


def _enum_not_found(hwnd, lst):
    pass


def test_maximize_anki_calls_show_window():
    with patch("window.win32gui.EnumWindows", side_effect=lambda cb, lst: _enum_found(12345, lst)), \
         patch("window.win32gui.GetWindowText", return_value="Benutzer 1 - Anki"), \
         patch("window.win32gui.ShowWindow") as mock_show, \
         patch("window.win32gui.SetWindowPos") as mock_pos:
        maximize_anki()
        mock_show.assert_called_once_with(12345, win32con.SW_MAXIMIZE)
        assert mock_pos.call_count == 2


def test_maximize_anki_skips_if_no_window():
    with patch("window.win32gui.EnumWindows", side_effect=lambda cb, lst: None), \
         patch("window.win32gui.ShowWindow") as mock_show, \
         patch("window.win32gui.SetWindowPos") as mock_pos:
        maximize_anki()
        mock_show.assert_not_called()
        mock_pos.assert_not_called()


def test_minimize_anki_calls_show_window():
    with patch("window.win32gui.EnumWindows", side_effect=lambda cb, lst: _enum_found(12345, lst)), \
         patch("window.win32gui.GetWindowText", return_value="Benutzer 1 - Anki"), \
         patch("window.win32gui.ShowWindow") as mock_show:
        minimize_anki()
        mock_show.assert_called_once_with(12345, win32con.SW_MINIMIZE)


def test_minimize_anki_skips_if_no_window():
    with patch("window.win32gui.EnumWindows", side_effect=lambda cb, lst: None), \
         patch("window.win32gui.ShowWindow") as mock_show:
        minimize_anki()
        mock_show.assert_not_called()
