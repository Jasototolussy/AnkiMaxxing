import win32gui
import win32con


def _find_anki():
    result = []
    win32gui.EnumWindows(
        lambda hwnd, lst: lst.append(hwnd) if "Anki" in win32gui.GetWindowText(hwnd) else None,
        result,
    )
    return result[0] if result else 0


def maximize_anki():
    hwnd = _find_anki()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(hwnd)


def minimize_anki():
    hwnd = _find_anki()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
