# AnkiMaxxing

Maximizes Anki when you die in League of Legends. Minimizes it when you respawn.

## Requirements

- Windows
- Python 3.11+
- Anki running in the background
- League of Legends (Live Client API must be enabled — it is by default)

## Setup

```bash
git clone https://github.com/Jasototolussy/AnkiMaxxing.git
cd AnkiMaxxing
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Usage

Double-click `start.bat` to launch. A tray icon appears in the system tray.

To create a desktop shortcut: right-click `start.bat` → Send to → Desktop (create shortcut).

### Tray menu

- Status: `Warte auf Spiel` / `Im Spiel` / `Im Spiel — Tot` / `Im Spiel — Lebendig`
- **Beenden** — exits the app

## How it works

The app polls the [LoL Live Client API](https://developer.riotgames.com/docs/lol#game-client-api) every 500ms. When your player's `isDead` status changes, it maximizes or minimizes the Anki window via the Windows API.
