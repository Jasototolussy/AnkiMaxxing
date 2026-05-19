import requests
import urllib3
urllib3.disable_warnings()

r1 = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False)
r2 = requests.get("https://127.0.0.1:2999/liveclientdata/playerlist", verify=False)

print("ACTIVEPLAYER summonerName:", r1.json().get("summonerName"))
print("ACTIVEPLAYER riotIdGameName:", r1.json().get("riotIdGameName"))
print()
print("PLAYERLIST:")
for p in r2.json():
    print(" ", p.get("summonerName"), "|", p.get("riotIdGameName"), "| isDead:", p.get("isDead"))
