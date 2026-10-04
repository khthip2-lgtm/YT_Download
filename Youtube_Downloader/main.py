"""YouTube Downloader - Python + PySide6 + yt-dlp.

Run:  python main.py
"""
from __future__ import annotations

import sys

from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QApplication

from ytdl_app.config import APP_ICON_PATH, APP_ICON_PNG, APP_NAME, APP_VERSION, ORG_NAME
from ytdl_app.ui.main_window import MainWindow


def main() -> int:
    # Ensure Windows taskbar groups under this app and shows the custom icon
    if sys.platform == "win32":
        try:
            import ctypes
            app_id = f"{ORG_NAME}.{APP_NAME}.{APP_VERSION}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except Exception:
            pass

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORG_NAME)

    default_font = QFont()
    default_font.setFamilies([
        "Leelawadee UI",
        "Kantumruy Pro",
        "Khmer OS Battambang",
        "Khmer OS Content",
        "Noto Sans Khmer",
        "Segoe UI",
        "Inter",
        "sans-serif",
    ])
    default_font.setPointSize(10)
    app.setFont(default_font)

    if APP_ICON_PNG.exists():
        app.setWindowIcon(QIcon(str(APP_ICON_PNG)))
    elif APP_ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(APP_ICON_PATH)))

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
