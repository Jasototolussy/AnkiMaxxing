import win32gui
import win32con


def _find_anki():
    return win32gui.FindWindow(None, "Anki")


def maximize_anki():
    hwnd = _find_anki()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)


def minimize_anki():
    hwnd = _find_anki()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
