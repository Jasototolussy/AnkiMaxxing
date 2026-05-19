import requests
import urllib3
import time
urllib3.disable_warnings()

_BASE = "https://127.0.0.1:2999/liveclientdata"

player_id = None
was_dead = False

while True:
    try:
        r1 = requests.get(f"{_BASE}/activeplayer", verify=False, timeout=1)
        fresh_id = r1.json().get("summonerName") or r1.json().get("riotIdGameName") or None
        if fresh_id is not None:
            player_id = fresh_id
    except Exception:
        fresh_id = None

    try:
        r2 = requests.get(f"{_BASE}/playerlist", verify=False, timeout=1)
        players = r2.json()
    except Exception:
        players = None

    if players is None:
        print(f"playerlist=None → game end")
        player_id = None
        was_dead = False
        time.sleep(0.5)
        continue

    if player_id is None:
        print(f"waiting for player_id...")
        time.sleep(0.5)
        continue

    player = next(
        (p for p in players if p.get("summonerName") == player_id or p.get("riotIdGameName") == player_id),
        None
    )

    if player is None:
        print(f"no match for player_id='{player_id}'")
        time.sleep(0.5)
        continue

    is_dead = player.get("isDead", False)
    if is_dead and not was_dead:
        print(f">>> DEATH detected (player_id={player_id})")
        was_dead = True
    elif not is_dead and was_dead:
        print(f">>> RESPAWN detected (player_id={player_id})")
        was_dead = False

    time.sleep(0.5)
