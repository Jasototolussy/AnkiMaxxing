import threading
import time
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_BASE = "https://127.0.0.1:2999/liveclientdata"
_INTERVAL = 0.5


class Poller:
    def __init__(self, on_death, on_respawn, on_game_start=None, on_game_end=None):
        self.on_death = on_death
        self.on_respawn = on_respawn
        self.on_game_start = on_game_start
        self.on_game_end = on_game_end
        self._stop = threading.Event()
        self._was_dead = False
        self._in_game = False

    def start(self):
        self._stop.clear()
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._stop.set()

    def _run(self):
        while not self._stop.is_set():
            self._tick()
            time.sleep(_INTERVAL)

    def _get_player_id(self):
        try:
            r = requests.get(f"{_BASE}/activeplayer", verify=False, timeout=1)
            data = r.json()
            return data.get("summonerName") or data.get("riotIdGameName") or None
        except Exception:
            return None

    def _get_player_list(self):
        try:
            r = requests.get(f"{_BASE}/playerlist", verify=False, timeout=1)
            return r.json()
        except Exception:
            return None

    def _tick(self):
        player_id = self._get_player_id()

        if player_id is None:
            if self._in_game:
                self._in_game = False
                self._was_dead = False
                if self.on_game_end:
                    self.on_game_end()
            return

        players = self._get_player_list()
        if players is None:
            if self._in_game:
                self._in_game = False
                self._was_dead = False
                if self.on_game_end:
                    self.on_game_end()
            return

        if not self._in_game:
            self._in_game = True
            if self.on_game_start:
                self.on_game_start()

        player = next(
            (
                p for p in players
                if p.get("summonerName") == player_id
                or p.get("riotIdGameName") == player_id
            ),
            None,
        )
        if player is None:
            return

        is_dead = player.get("isDead", False)
        if is_dead and not self._was_dead:
            self._was_dead = True
            self.on_death()
        elif not is_dead and self._was_dead:
            self._was_dead = False
            self.on_respawn()
