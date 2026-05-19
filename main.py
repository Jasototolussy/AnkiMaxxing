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
    try:
        tray.run()  # blocks until user clicks "Beenden"
    finally:
        poller.stop()


if __name__ == "__main__":
    main()
