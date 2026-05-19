import requests
import urllib3
urllib3.disable_warnings()

r1 = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False, timeout=1)
r2 = requests.get("https://127.0.0.1:2999/liveclientdata/playerlist", verify=False, timeout=1)

player_id = r1.json().get("summonerName") or r1.json().get("riotIdGameName")
print(f"player_id from activeplayer: '{player_id}'")
print()
for p in r2.json():
    sn = p.get("summonerName")
    rn = p.get("riotIdGameName")
    match_sn = sn == player_id
    match_rn = rn == player_id
    print(f"summonerName='{sn}' match={match_sn} | riotIdGameName='{rn}' match={match_rn}")
