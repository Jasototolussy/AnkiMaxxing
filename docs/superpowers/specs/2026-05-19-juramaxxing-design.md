# JuraMaxxing — Design Spec

**Date:** 2026-05-19

## Overview

A Python tray application that maximizes Anki when the local player dies in League of Legends, and minimizes it again when they respawn. Uses the official LoL Live Client API for death detection.

---

## Architecture

Three components:

1. **Poller** (`poller.py`) — background thread that polls the LoL Live Client API every 500ms. Detects state transitions (`alive → dead`, `dead → alive`) and fires callbacks.
2. **Window Controller** (`window.py`) — receives callbacks and controls the Anki window via `pywin32`: maximize on death, minimize on respawn.
3. **Tray App** (`tray.py`) — `pystray` icon in the system tray with a status display and a "Beenden" (quit) button. Runs on the main thread.

Entry point: `main.py`. Launched via `start.bat` using `pythonw.exe` (no terminal window).

---

## Data Flow

1. Tray app starts → Poller thread begins
2. Poller calls `GET https://127.0.0.1:2999/liveclientdata/playerlist` every 500ms (SSL verification disabled — Riot uses a self-signed cert)
3. No game active → API unavailable → Poller sleeps silently and retries
4. Game active → Poller reads `isDead` for the local player (identified via `GET /liveclientdata/activeplayer` → `summonerName`, cached on first successful call)
5. State transitions:
   - `false → true` (death): maximize Anki
   - `true → false` (respawn): minimize Anki
   - No change: do nothing

---

## Window Control

`pywin32` finds the Anki window by title (`win32gui.FindWindow(None, "Anki")`). Only the Anki window is affected; all other windows (browsers, etc.) are untouched.

---

## Tray Icon

- Tooltip: `JuraMaxxing`
- Menu:
  - Status label (non-clickable): `Warte auf Spiel` or `Im Spiel`
  - **Beenden** — stops the poller thread and exits
- Icon: simple colored circle generated via `Pillow` (no external icon file needed)
- On quit: Anki is left in its current state (not modified)

---

## Project Structure

```
JuraMaxxing/
├── main.py          # Entry point, starts tray app and poller thread
├── poller.py        # LoL Live Client API polling thread
├── window.py        # Anki window maximize/minimize via pywin32
├── tray.py          # pystray tray icon and menu
├── start.bat        # Desktop shortcut launcher (pythonw.exe main.py)
└── requirements.txt
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP polling of LoL Live Client API |
| `pywin32` | Control Anki window (maximize/minimize) |
| `pystray` | System tray icon and menu |
| `Pillow` | Generate tray icon image |

---

## Error Handling

- API unreachable (no game): silent retry, no crash
- Anki not open: `FindWindow` returns `None` → skip action, no crash
- Game ends mid-session: API stops responding → Poller treats as "no game", resets state
