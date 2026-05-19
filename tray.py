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
