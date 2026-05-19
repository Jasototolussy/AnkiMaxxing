import requests
import urllib3
import time
import win32gui
import win32con
urllib3.disable_warnings()

_BASE = "https://127.0.0.1:2999/liveclientdata"

player_id = None
was_dead = False

def find_anki():
    result = []
    win32gui.EnumWindows(
        lambda hwnd, lst: lst.append(hwnd) if "Anki" in win32gui.GetWindowText(hwnd) else None,
        result,
    )
    return result[0] if result else 0

def maximize_anki():
    hwnd = find_anki()
    print(f"  maximize_anki: hwnd={hwnd}")
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetForegroundWindow(hwnd)

def minimize_anki():
    hwnd = find_anki()
    print(f"  minimize_anki: hwnd={hwnd}")
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

while True:
    try:
        r1 = requests.get(f"{_BASE}/activeplayer", verify=False, timeout=1)
        fresh_id = r1.json().get("summonerName") or r1.json().get("riotIdGameName") or None
        if fresh_id is not None:
            player_id = fresh_id
    except Exception:
        pass

    try:
        r2 = requests.get(f"{_BASE}/playerlist", verify=False, timeout=1)
        players = r2.json()
    except Exception:
        players = None

    if players is None or player_id is None:
        time.sleep(0.5)
        continue

    player = next(
        (p for p in players if p.get("summonerName") == player_id or p.get("riotIdGameName") == player_id),
        None
    )
    if player is None:
        time.sleep(0.5)
        continue

    is_dead = player.get("isDead", False)
    if is_dead and not was_dead:
        print(f">>> DEATH → maximize_anki()")
        maximize_anki()
        was_dead = True
    elif not is_dead and was_dead:
        print(f">>> RESPAWN → minimize_anki()")
        minimize_anki()
        was_dead = False

    time.sleep(0.5)
