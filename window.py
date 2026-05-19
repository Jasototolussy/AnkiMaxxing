import win32gui
import win32con
import win32process
import win32api


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
            # Attach to the target window's thread to bypass foreground lock
            fg_hwnd = win32gui.GetForegroundWindow()
            fg_tid = win32process.GetWindowThreadProcessId(fg_hwnd)[0]
            our_tid = win32api.GetCurrentThreadId()
            target_tid = win32process.GetWindowThreadProcessId(hwnd)[0]
            if fg_tid != our_tid:
                win32process.AttachThreadInput(our_tid, fg_tid, True)
                win32process.AttachThreadInput(target_tid, fg_tid, True)
            win32gui.SetForegroundWindow(hwnd)
            if fg_tid != our_tid:
                win32process.AttachThreadInput(our_tid, fg_tid, False)
                win32process.AttachThreadInput(target_tid, fg_tid, False)
        except Exception:
            pass


def minimize_anki():
    hwnd = _find_anki()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
