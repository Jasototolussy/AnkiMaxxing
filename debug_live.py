import requests
import urllib3
import time
urllib3.disable_warnings()

prev_dead = None

while True:
    try:
        r1 = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False, timeout=1)
        r2 = requests.get("https://127.0.0.1:2999/liveclientdata/playerlist", verify=False, timeout=1)
        player_id = r1.json().get("summonerName") or r1.json().get("riotIdGameName")
        players = r2.json()
        match = next((p for p in players if p.get("summonerName") == player_id or p.get("riotIdGameName") == player_id), None)
        if match:
            is_dead = match.get("isDead")
            if is_dead != prev_dead:
                print(f"WECHSEL: isDead={is_dead} | player_id={player_id}")
                prev_dead = is_dead
        else:
            print(f"Kein Match! player_id={player_id}")
    except Exception as e:
        print(f"Fehler: {e}")
    time.sleep(0.5)
