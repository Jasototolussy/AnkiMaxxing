# AnkiMaxxing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Windows system tray app that maximizes Anki when the local LoL player dies and minimizes it on respawn.

**Architecture:** A background poller thread polls the LoL Live Client API every 500ms for the local player's `isDead` state. On state transitions it calls callbacks that control the Anki window via pywin32. A pystray tray icon on the main thread shows the current status and a quit button.

**Tech Stack:** Python 3, `requests`, `pywin32`, `pystray`, `Pillow`, `pytest`

---

## File Map

| File | Responsibility |
|---|---|
| `requirements.txt` | Pinned dependencies |
| `window.py` | Find and maximize/minimize the Anki window via pywin32 |
| `poller.py` | Poll LoL Live Client API, fire `on_death` / `on_respawn` callbacks |
| `tray.py` | pystray icon, menu, `update_status()` |
| `main.py` | Wire poller + tray together, entry point |
| `start.bat` | Launch with `.venv\Scripts\pythonw.exe` (no console window, no PATH dependency) |
| `tests/test_window.py` | Unit tests for window control |
| `tests/test_poller.py` | Unit tests for poller state machine |

---

## Task 1: Project Setup

**Files:**
- Create: `requirements.txt`
- Create: `tests/__init__.py`

- [ ] **Step 1: Write requirements.txt**

```
requests==2.32.3
pywin32==308
pystray==0.19.5
Pillow==10.4.0
pytest==8.3.3
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -r requirements.txt`

Expected: All packages install without error.

- [ ] **Step 3: Create tests package**

Create an empty file `tests/__init__.py`.

- [ ] **Step 4: Commit**

```bash
git add requirements.txt tests/__init__.py
git commit -m "chore: add dependencies and test package"
```

---

## Task 2: Anki Window Control (`window.py`)

**Files:**
- Create: `window.py`
- Create: `tests/test_window.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_window.py`:

```python
from unittest.mock import patch
import win32con


def test_maximize_anki_calls_show_window():
    with patch("window.win32gui.FindWindow", return_value=12345) as mock_find, \
         patch("window.win32gui.ShowWindow") as mock_show:
        from window import maximize_anki
        maximize_anki()
        mock_find.assert_called_once_with(None, "Anki")
        mock_show.assert_called_once_with(12345, win32con.SW_MAXIMIZE)


def test_maximize_anki_skips_if_no_window():
    with patch("window.win32gui.FindWindow", return_value=0), \
         patch("window.win32gui.ShowWindow") as mock_show:
        from window import maximize_anki
        maximize_anki()
        mock_show.assert_not_called()


def test_minimize_anki_calls_show_window():
    with patch("window.win32gui.FindWindow", return_value=12345) as mock_find, \
         patch("window.win32gui.ShowWindow") as mock_show:
        from window import minimize_anki
        minimize_anki()
        mock_find.assert_called_once_with(None, "Anki")
        mock_show.assert_called_once_with(12345, win32con.SW_MINIMIZE)


def test_minimize_anki_skips_if_no_window():
    with patch("window.win32gui.FindWindow", return_value=0), \
         patch("window.win32gui.ShowWindow") as mock_show:
        from window import minimize_anki
        minimize_anki()
        mock_show.assert_not_called()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_window.py -v`

Expected: 4 errors — `ModuleNotFoundError: No module named 'window'`

- [ ] **Step 3: Implement window.py**

Create `window.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_window.py -v`

Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git add window.py tests/test_window.py
git commit -m "feat: add Anki window control"
```

---

## Task 3: LoL Poller (`poller.py`)

**Files:**
- Create: `poller.py`
- Create: `tests/test_poller.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_poller.py`:

```python
from unittest.mock import MagicMock, patch
from poller import Poller


def _make_player(name, is_dead, riot_id=None):
    return {
        "summonerName": name,
        "riotIdGameName": riot_id or "",
        "isDead": is_dead,
    }


def _make_poller(**kwargs):
    defaults = dict(on_death=MagicMock(), on_respawn=MagicMock())
    defaults.update(kwargs)
    return Poller(**defaults)


def test_on_death_fires_on_alive_to_dead_transition():
    p = _make_poller()
    p._player_id = "TestPlayer"
    p._in_game = True
    p._was_dead = False

    with patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", True)]):
        p._tick()

    p.on_death.assert_called_once()
    p.on_respawn.assert_not_called()


def test_on_respawn_fires_on_dead_to_alive_transition():
    p = _make_poller()
    p._player_id = "TestPlayer"
    p._in_game = True
    p._was_dead = True

    with patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", False)]):
        p._tick()

    p.on_respawn.assert_called_once()
    p.on_death.assert_not_called()


def test_no_callback_when_already_alive():
    p = _make_poller()
    p._player_id = "TestPlayer"
    p._in_game = True
    p._was_dead = False

    with patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", False)]):
        p._tick()

    p.on_death.assert_not_called()
    p.on_respawn.assert_not_called()


def test_no_callback_when_already_dead():
    p = _make_poller()
    p._player_id = "TestPlayer"
    p._in_game = True
    p._was_dead = True

    with patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", True)]):
        p._tick()

    p.on_death.assert_not_called()
    p.on_respawn.assert_not_called()


def test_api_unavailable_triggers_game_end():
    on_game_end = MagicMock()
    p = _make_poller(on_game_end=on_game_end)
    p._player_id = "TestPlayer"
    p._in_game = True

    with patch.object(p, "_get_player_list", return_value=None):
        p._tick()

    assert not p._in_game
    assert p._player_id is None
    on_game_end.assert_called_once()


def test_fallback_to_riot_id_game_name():
    p = _make_poller()
    p._player_id = "CoolPlayer"
    p._in_game = True
    p._was_dead = False
    player = {"summonerName": "", "riotIdGameName": "CoolPlayer", "isDead": True}

    with patch.object(p, "_get_player_list", return_value=[player]):
        p._tick()

    p.on_death.assert_called_once()


def test_on_game_start_fires_when_game_begins():
    on_game_start = MagicMock()
    p = _make_poller(on_game_start=on_game_start)
    p._player_id = "TestPlayer"
    p._in_game = False

    with patch.object(p, "_get_player_list", return_value=[_make_player("TestPlayer", False)]):
        p._tick()

    on_game_start.assert_called_once()
    assert p._in_game
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_poller.py -v`

Expected: 7 errors — `ModuleNotFoundError: No module named 'poller'`

- [ ] **Step 3: Implement poller.py**

Create `poller.py`:

```python
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
        self._player_id = None

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
        if self._player_id is None:
            self._player_id = self._get_player_id()

        if self._player_id is None:
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
                self._player_id = None
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
                if p.get("summonerName") == self._player_id
                or p.get("riotIdGameName") == self._player_id
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_poller.py -v`

Expected: 7 PASSED

- [ ] **Step 5: Commit**

```bash
git add poller.py tests/test_poller.py
git commit -m "feat: add LoL Live Client API poller"
```

---

## Task 4: System Tray Icon (`tray.py`)

**Files:**
- Create: `tray.py`

No unit tests for the tray — pystray's `run()` blocks and requires a display. Verified manually in Task 6.

- [ ] **Step 1: Implement tray.py**

Create `tray.py`:

```python
import pystray
from PIL import Image, ImageDraw


def _make_icon():
    img = Image.new("RGB", (64, 64), (30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=(0, 200, 80))
    return img


class TrayApp:
    def __init__(self):
        self._status = "Warte auf Spiel"
        self._icon = None

    def update_status(self, text):
        self._status = text
        if self._icon is not None:
            self._icon.menu = self._build_menu()
            self._icon.update_menu()

    def _build_menu(self):
        return pystray.Menu(
            pystray.MenuItem(self._status, None, enabled=False),
            pystray.MenuItem("Beenden", self._on_quit),
        )

    def _on_quit(self, icon, item):
        self._icon.stop()

    def run(self):
        self._icon = pystray.Icon(
            "AnkiMaxxing",
            _make_icon(),
            "AnkiMaxxing",
            self._build_menu(),
        )
        self._icon.run()
```

- [ ] **Step 2: Commit**

```bash
git add tray.py
git commit -m "feat: add system tray icon"
```

---

## Task 5: Entry Point (`main.py`)

**Files:**
- Create: `main.py`

- [ ] **Step 1: Implement main.py**

Create `main.py`:

```python
from poller import Poller
from window import maximize_anki, minimize_anki
from tray import TrayApp


def main():
    tray = TrayApp()

    def on_death():
        maximize_anki()
        tray.update_status("Im Spiel — Tot")

    def on_respawn():
        minimize_anki()
        tray.update_status("Im Spiel — Lebendig")

    def on_game_start():
        tray.update_status("Im Spiel")

    def on_game_end():
        tray.update_status("Warte auf Spiel")

    poller = Poller(
        on_death=on_death,
        on_respawn=on_respawn,
        on_game_start=on_game_start,
        on_game_end=on_game_end,
    )
    poller.start()
    tray.run()  # blocks until user clicks "Beenden"
    poller.stop()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run all tests**

Run: `pytest tests/ -v`

Expected: 11 PASSED

- [ ] **Step 3: Commit**

```bash
git add main.py
git commit -m "feat: wire poller and tray in main entry point"
```

---

## Task 6: Desktop Launcher (`start.bat`) + Manual Smoke Test

**Files:**
- Create: `start.bat`

- [ ] **Step 1: Create start.bat**

Create `start.bat`:

```bat
@echo off
cd /d "%~dp0"
.venv\Scripts\pythonw.exe main.py
```

- [ ] **Step 2: Create desktop shortcut**

Right-click `start.bat` → Send to → Desktop (create shortcut).
Or manually create a shortcut pointing to the `.bat` file.

- [ ] **Step 3: Manual smoke test**

1. Open Anki on your desktop.
2. Double-click the `start.bat` shortcut.
3. Verify the AnkiMaxxing icon appears in the system tray.
4. Right-click the icon → status shows "Warte auf Spiel".
5. Start a League of Legends game.
6. Status in tray should change to "Im Spiel".
7. Die in-game → Anki should maximize.
8. Respawn → Anki should minimize.
9. Right-click tray icon → "Beenden" → app exits.

- [ ] **Step 4: Commit**

```bash
git add start.bat
git commit -m "feat: add start.bat desktop launcher"
```
