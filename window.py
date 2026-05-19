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
        try:
            # Briefly set topmost to appear above LoL, then restore normal z-order
            SWP_FLAGS = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, SWP_FLAGS)
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, SWP_FLAGS)
        except Exception:
            pass


def _find_lol():
    result = []
    win32gui.EnumWindows(
        lambda hwnd, lst: lst.append(hwnd) if win32gui.GetWindowText(hwnd) == "League of Legends" else None,
        result,
    )
    return result[0] if result else 0


def minimize_anki():
    hwnd = _find_anki()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    lol_hwnd = _find_lol()
    if lol_hwnd:
        try:
            SWP_FLAGS = win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            win32gui.SetWindowPos(lol_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, SWP_FLAGS)
            win32gui.SetWindowPos(lol_hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, SWP_FLAGS)
        except Exception:
            pass
