"""Main window - layout follows the provided mockup."""
from __future__ import annotations

import os
import subprocess
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pathlib import Path

# Support running directly or as a package
if __package__ is None or __package__ == "":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))
    from ytdl_app.config import (
        APP_ICON_PATH,
        APP_ICON_PNG,
        APP_NAME,
        APP_VERSION,
        CONTAINERS,
        RESOLUTIONS,
        default_download_dir,
        human_time,
        settings,
    )
    from ytdl_app.core.downloader import DownloadWorker
    from ytdl_app.core.fetcher import FetchWorker, VideoItem
    from ytdl_app.ui.styles import DARK_STYLESHEET, LIGHT_STYLESHEET, get_stylesheet
else:
    from ..config import (
        APP_ICON_PATH,
        APP_ICON_PNG,
        APP_NAME,
        APP_VERSION,
        CONTAINERS,
        RESOLUTIONS,
        default_download_dir,
        human_time,
        settings,
    )
    from ..core.downloader import DownloadWorker
    from ..core.fetcher import FetchWorker, VideoItem
    from .styles import DARK_STYLESHEET, LIGHT_STYLESHEET, get_stylesheet

COL_NO, COL_TITLE, COL_URL, COL_STATUS, COL_ACTION = range(5)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        if APP_ICON_PNG.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PNG)))
        elif APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))
        self.resize(1180, 680)
        self.setMinimumSize(940, 580)

        self.current_theme = "dark"
        self.items: list[VideoItem] = []
        self.fetcher: FetchWorker | None = None
        self.downloader: DownloadWorker | None = None

        self._build_ui()
        self._restore_settings()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("Root")
        self.setCentralWidget(root)

        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(20, 18, 20, 14)
        main_layout.setSpacing(14)

        # --- Top Header (Title + Badge + Theme Toggle) ---
        header_widget = QWidget()
        hl = QHBoxLayout(header_widget)
        hl.setContentsMargins(2, 0, 2, 0)
        hl.setSpacing(10)

        title_lbl = QLabel(f"▶  {APP_NAME}")
        title_lbl.setObjectName("AppTitle")
        badge_lbl = QLabel(f"v{APP_VERSION}")
        badge_lbl.setObjectName("AppBadge")
        hl.addWidget(title_lbl)
        hl.addWidget(badge_lbl)
        hl.addStretch(1)

        self.theme_btn = QPushButton("☀️ Light Mode")
        self.theme_btn.setObjectName("ThemeBtn")
        self.theme_btn.setToolTip("ចុចដើម្បីប្ដូររវាង Dark Mode និង Light Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        hl.addWidget(self.theme_btn)

        main_layout.addWidget(header_widget)

        # --- Middle Grid (URL + Table + Action Buttons) ---
        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(12)

        # --- URL input (row 0) -----------------------------------------
        self.url_edit = QLineEdit()
        self.url_edit.setObjectName("UrlInput")
        self.url_edit.setPlaceholderText(
            "🔗 បញ្ចូល YouTube Video ឬ Playlist Link (https://www.youtube.com/watch?v=...)"
        )
        self.url_edit.setFixedHeight(46)
        self.url_edit.setClearButtonEnabled(True)
        self.url_edit.returnPressed.connect(self.on_fetch)
        grid.addWidget(self.url_edit, 0, 0)

        # --- Table (row 1) ---------------------------------------------
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["No", "Title", "Url", "Status", "Action"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(COL_NO, QHeaderView.Fixed)
        header.setSectionResizeMode(COL_TITLE, QHeaderView.Stretch)
        header.setSectionResizeMode(COL_URL, QHeaderView.Interactive)
        header.setSectionResizeMode(COL_STATUS, QHeaderView.Fixed)
        header.setSectionResizeMode(COL_ACTION, QHeaderView.Fixed)
        self.table.setColumnWidth(COL_NO, 52)
        self.table.setColumnWidth(COL_URL, 260)
        self.table.setColumnWidth(COL_STATUS, 210)
        self.table.setColumnWidth(COL_ACTION, 175)
        self.table.verticalHeader().setDefaultSectionSize(38)
        grid.addWidget(self.table, 1, 0)

        # --- Action buttons (right column, rows 0-1) --------------------
        buttons = QWidget()
        bl = QVBoxLayout(buttons)
        bl.setContentsMargins(0, 0, 0, 0)
        bl.setSpacing(10)

        self.fetch_btn = QPushButton("🔍 Fetch Link")
        self.fetch_btn.setObjectName("FetchBtn")
        self.fetch_btn.setToolTip("ទាញបញ្ជីវីដេអូពី link (single / playlist)")
        self.fetch_btn.clicked.connect(self.on_fetch)

        self.download_btn = QPushButton("⬇ Download All")
        self.download_btn.setObjectName("DownloadBtn")
        self.download_btn.setToolTip("ចាប់ផ្ដើមដោនឡូតវីដេអូទាំងអស់ក្នុងបញ្ជី")
        self.download_btn.clicked.connect(self.on_download)

        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setObjectName("StopBtn")
        self.stop_btn.setToolTip("បញ្ឈប់ដំណើរការ")
        self.stop_btn.clicked.connect(self.on_stop)
        self.stop_btn.setEnabled(False)

        for btn in (self.fetch_btn, self.download_btn, self.stop_btn):
            btn.setMinimumWidth(155)
            btn.setFixedHeight(46)
            bl.addWidget(btn)
        bl.addStretch(1)

        self.clear_btn = QPushButton("🗑 Clear list")
        self.clear_btn.setObjectName("ClearBtn")
        self.clear_btn.setMinimumWidth(155)
        self.clear_btn.setFixedHeight(44)
        self.clear_btn.clicked.connect(self.clear_list)
        bl.addWidget(self.clear_btn)

        buttons.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        grid.addWidget(buttons, 0, 1, 2, 1)

        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        main_layout.addLayout(grid, 1)

        # --- Bottom options Card ----------------------------------------
        options_card = QFrame()
        options_card.setObjectName("OptionsCard")
        ol = QHBoxLayout(options_card)
        ol.setContentsMargins(16, 12, 16, 12)
        ol.setSpacing(16)

        # Resolution
        res_box = QVBoxLayout()
        res_box.setSpacing(6)
        res_lbl = QLabel("Quality / Resolution")
        res_lbl.setObjectName("SectionLabel")
        res_box.addWidget(res_lbl)
        self.res_combo = QComboBox()
        self.res_combo.setFixedHeight(40)
        self.res_combo.setMinimumWidth(165)
        for label, _height in RESOLUTIONS:
            self.res_combo.addItem(label)
        self.res_combo.setCurrentIndex(3)  # 1080p
        res_box.addWidget(self.res_combo)
        ol.addLayout(res_box)

        # Container / video type
        fmt_box = QVBoxLayout()
        fmt_box.setSpacing(6)
        fmt_lbl = QLabel("Format / Type")
        fmt_lbl.setObjectName("SectionLabel")
        fmt_box.addWidget(fmt_lbl)
        self.fmt_combo = QComboBox()
        self.fmt_combo.setFixedHeight(40)
        self.fmt_combo.setMinimumWidth(150)
        for name in CONTAINERS:
            self.fmt_combo.addItem(name)
        self.fmt_combo.setCurrentIndex(0)  # MP4
        fmt_box.addWidget(self.fmt_combo)
        ol.addLayout(fmt_box)

        # Destination files + Browse + Open folder on the same row
        dest_box = QVBoxLayout()
        dest_box.setSpacing(6)
        dest_lbl = QLabel("Save Location :")
        dest_lbl.setObjectName("SectionLabel")
        dest_box.addWidget(dest_lbl)

        dest_row = QHBoxLayout()
        dest_row.setSpacing(8)
        self.dest_edit = QLineEdit(default_download_dir())
        self.dest_edit.setFixedHeight(40)
        dest_row.addWidget(self.dest_edit, 1)

        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.setObjectName("BrowseBtn")
        self.browse_btn.setFixedHeight(40)
        self.browse_btn.setMinimumWidth(110)
        self.browse_btn.clicked.connect(self.on_browse)
        dest_row.addWidget(self.browse_btn)

        self.open_btn = QPushButton("📂 Open folder")
        self.open_btn.setObjectName("OpenBtn")
        self.open_btn.setFixedHeight(40)
        self.open_btn.setMinimumWidth(125)
        self.open_btn.clicked.connect(lambda: self.open_path(self.dest_edit.text()))
        dest_row.addWidget(self.open_btn)

        dest_box.addLayout(dest_row)
        ol.addLayout(dest_box, 1)

        main_layout.addWidget(options_card)

        # --- Status bar --------------------------------------------------
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("✨ រួចរាល់។ សូមបញ្ចូល YouTube link រួចចុច Fetch Link។")

    def toggle_theme(self) -> None:
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme(new_theme)
        st = settings()
        st.setValue("theme", self.current_theme)

    def apply_theme(self, theme: str) -> None:
        self.current_theme = theme.lower()
        if self.current_theme == "light":
            self.theme_btn.setText("🌙 Dark Mode")
        else:
            self.theme_btn.setText("☀️ Light Mode")
        self.setStyleSheet(get_stylesheet(self.current_theme))

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------
    def _restore_settings(self) -> None:
        st = settings()
        dest = st.value("dest_dir", "", str)
        if dest and os.path.isdir(dest):
            self.dest_edit.setText(dest)
        res = st.value("res_row", -1, int)
        if 0 <= res < self.res_combo.count():
            self.res_combo.setCurrentIndex(res)
        fmt = st.value("fmt_row", -1, int)
        if 0 <= fmt < self.fmt_combo.count():
            self.fmt_combo.setCurrentIndex(fmt)
        theme = st.value("theme", "dark", str)
        self.apply_theme(theme)

    def _save_settings(self) -> None:
        st = settings()
        st.setValue("dest_dir", self.dest_edit.text())
        st.setValue("res_row", self.res_combo.currentIndex())
        st.setValue("fmt_row", self.fmt_combo.currentIndex())
        st.setValue("theme", self.current_theme)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def selected_height(self) -> int | None:
        row = max(0, self.res_combo.currentIndex())
        return RESOLUTIONS[row][1]

    def selected_container(self) -> str:
        row = max(0, self.fmt_combo.currentIndex())
        return CONTAINERS[row]


    def set_busy(self, busy: bool, fetching: bool = False) -> None:
        self.fetch_btn.setEnabled(not busy)
        self.download_btn.setEnabled(not busy)
        self.stop_btn.setEnabled(busy and not fetching)
        self.clear_btn.setEnabled(not busy)

    def open_path(self, path: str) -> None:
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, APP_NAME, "រកមិនឃើញទីតាំងនះទេ។")
            return
        folder = path if os.path.isdir(path) else os.path.dirname(path)
        QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    # ------------------------------------------------------------------
    # Table rows
    # ------------------------------------------------------------------
    def add_row(self, item: VideoItem) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.items.append(item)

        no_item = QTableWidgetItem(str(row + 1))
        no_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, COL_NO, no_item)

        title = item.title
        if item.duration:
            title = f"{title}  ({human_time(item.duration)})"
        title_item = QTableWidgetItem(title)
        title_item.setToolTip(item.title)
        self.table.setItem(row, COL_TITLE, title_item)

        url_item = QTableWidgetItem(item.url)
        url_item.setToolTip(item.url)
        self.table.setItem(row, COL_URL, url_item)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setFormat("Ready")
        self.table.setCellWidget(row, COL_STATUS, bar)

        self.table.setCellWidget(row, COL_ACTION, self._action_widget(row))

    def _action_widget(self, row: int) -> QWidget:
        holder = QWidget()
        lay = QHBoxLayout(holder)
        lay.setContentsMargins(6, 3, 6, 3)
        lay.setSpacing(6)
        lay.setAlignment(Qt.AlignCenter)

        one = QPushButton("⬇ Download")
        one.setObjectName("RowBtn")
        one.setToolTip("ដោនឡូតតែវីដេអូនេះ")
        one.setFixedHeight(28)
        one.clicked.connect(lambda _=False, r=row: self.on_download(rows=[r]))

        rm = QPushButton("✕")
        rm.setObjectName("RowDanger")
        rm.setToolTip("លុបចេញពីបញ្ជី")
        rm.setFixedSize(28, 28)
        rm.clicked.connect(lambda _=False, r=row: self.remove_row(r))

        lay.addWidget(one)
        lay.addWidget(rm)
        return holder

    def remove_row(self, row: int) -> None:
        if self.downloader and self.downloader.isRunning():
            return
        if 0 <= row < len(self.items):
            self.table.removeRow(row)
            self.items.pop(row)
            self._renumber()

    def _renumber(self) -> None:
        for row in range(self.table.rowCount()):
            self.table.item(row, COL_NO).setText(str(row + 1))
            self.table.setCellWidget(row, COL_ACTION, self._action_widget(row))

    def clear_list(self) -> None:
        if self.downloader and self.downloader.isRunning():
            return
        self.table.setRowCount(0)
        self.items.clear()
        self.statusBar().showMessage("បានលុបបញ្ជីទាំងស្រុង។")

    # ------------------------------------------------------------------
    # Fetch
    # ------------------------------------------------------------------
    def on_fetch(self) -> None:
        url = self.url_edit.text().strip()
        if not url:
            clip = QGuiApplication.clipboard().text().strip()
            if clip.startswith("http"):
                url = clip
                self.url_edit.setText(clip)
        if not url.startswith("http"):
            QMessageBox.warning(self, APP_NAME, "សូមបញ្ចូល YouTube link ជាមុនសិន។")
            return

        self.set_busy(True, fetching=True)
        self.statusBar().showMessage("កំពុង Fetch...")

        self.fetcher = FetchWorker(url, self)
        self.fetcher.item_found.connect(self.add_row)
        self.fetcher.message.connect(self.statusBar().showMessage)
        self.fetcher.failed.connect(self.on_fetch_failed)
        self.fetcher.finished_ok.connect(self.on_fetch_done)
        self.fetcher.finished.connect(lambda: self.set_busy(False))
        self.fetcher.start()

    def on_fetch_failed(self, message: str) -> None:
        self.statusBar().showMessage("Fetch មិនជោគជ័យ។")
        QMessageBox.critical(self, APP_NAME, f"Fetch មិនជោគជ័យ:\n\n{message}")

    def on_fetch_done(self, count: int, is_playlist: bool) -> None:
        kind = "Playlist" if is_playlist else "Single video"
        self.statusBar().showMessage(f"{kind}: បានបន្ថែម {count} វីដេអូទៅក្នុងបញ្ជី។")

    # ------------------------------------------------------------------
    # Download
    # ------------------------------------------------------------------
    def on_download(self, checked: bool = False, rows: list[int] | None = None) -> None:
        if self.downloader and self.downloader.isRunning():
            return
        if not self.items:
            QMessageBox.information(self, APP_NAME, "បញ្ជីទមេ។ សូមចុច Fetch ជាមុនសិន។")
            return

        dest = self.dest_edit.text().strip()
        if not dest:
            QMessageBox.warning(self, APP_NAME, "សូមជ្រើសរើសទីតាំងរក្សាទុក។")
            return
        try:
            os.makedirs(dest, exist_ok=True)
        except OSError as exc:
            QMessageBox.critical(self, APP_NAME, f"មិនអាចបង្កើត folder បាន:\n{exc}")
            return

        target_rows = rows if rows is not None else list(range(len(self.items)))
        jobs = [(r, self.items[r].url) for r in target_rows if 0 <= r < len(self.items)]
        if not jobs:
            return

        for row, _url in jobs:
            bar = self.table.cellWidget(row, COL_STATUS)
            if isinstance(bar, QProgressBar):
                bar.setValue(0)
                bar.setFormat("Queued")

        self._save_settings()
        self.set_busy(True)
        self.statusBar().showMessage(
            f"កំពុងដោនឡូត {len(jobs)} វីដេអូ • {self.res_combo.currentText()}"
            f" • {self.selected_container()}"
        )

        self.downloader = DownloadWorker(
            jobs, dest, self.selected_height(), self.selected_container(), self
        )
        self.downloader.progress.connect(self.on_progress)
        self.downloader.status.connect(self.on_status)
        self.downloader.item_done.connect(self.on_item_done)
        self.downloader.all_finished.connect(self.on_all_finished)
        self.downloader.finished.connect(lambda: self.set_busy(False))
        self.downloader.start()

    def on_progress(self, row: int, percent: float, detail: str) -> None:
        bar = self.table.cellWidget(row, COL_STATUS)
        if isinstance(bar, QProgressBar):
            bar.setValue(int(percent))
            bar.setFormat(detail)

    def on_status(self, row: int, status: str) -> None:
        bar = self.table.cellWidget(row, COL_STATUS)
        if isinstance(bar, QProgressBar):
            if status in ("Done", "Error", "Cancelled"):
                bar.setFormat(status)
                bar.setValue(100 if status == "Done" else bar.value())
            elif status == "Downloading":
                bar.setFormat("Downloading...")
        if 0 <= row < len(self.items):
            self.items[row].status = status

    def on_item_done(self, row: int, ok: bool, message: str) -> None:
        if 0 <= row < len(self.items):
            if ok:
                self.items[row].filepath = message
            else:
                self.items[row].extra["error"] = message
        if not ok and message and message != "Cancelled by user":
            self.statusBar().showMessage(f"ជួរ {row + 1}: {message[:120]}")

    def on_all_finished(self, completed: int, failed: int) -> None:
        self.statusBar().showMessage(
            f"បញ្ចប់។ ជោគជ័យ {completed} • មិនជោគជ័យ {failed}"
        )
        if completed and not failed:
            msg = QMessageBox(self)
            msg.setWindowTitle(APP_NAME)
            msg.setText(f"ដោនឡូតរួចរាល់ {completed} វីដេអូ។")
            msg.setIcon(QMessageBox.Information)
            open_btn = msg.addButton("Open folder", QMessageBox.ActionRole)
            close_btn = msg.addButton("Close", QMessageBox.RejectRole)
            msg.setDefaultButton(close_btn)
            msg.exec()
            if msg.clickedButton() == open_btn:
                self.open_path(self.dest_edit.text())
        elif completed and failed:
            msg = QMessageBox(self)
            msg.setWindowTitle(APP_NAME)
            msg.setText(f"ដោនឡូតបាន {completed} វីដេអូ (បរាជ័យ {failed})។")
            msg.setIcon(QMessageBox.Warning)
            open_btn = msg.addButton("Open folder", QMessageBox.ActionRole)
            close_btn = msg.addButton("Close", QMessageBox.RejectRole)
            msg.setDefaultButton(close_btn)
            msg.exec()
            if msg.clickedButton() == open_btn:
                self.open_path(self.dest_edit.text())


    # ------------------------------------------------------------------
    def on_stop(self) -> None:
        if self.downloader and self.downloader.isRunning():
            self.downloader.stop()
            self.statusBar().showMessage("កំពុងបញ្ឈប់...")
        if self.fetcher and self.fetcher.isRunning():
            self.fetcher.requestInterruption()

    def on_browse(self) -> None:
        start = self.dest_edit.text() or default_download_dir()
        folder = QFileDialog.getExistingDirectory(self, "ជ្រើសរើសទីតាំងរក្សាទុក", start)
        if folder:
            self.dest_edit.setText(folder)
            self._save_settings()

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self.downloader and self.downloader.isRunning():
            reply = QMessageBox.question(
                self,
                APP_NAME,
                "កំពុងដោនឡូត។ ចាក់ចេញមែនទេ?",
            )
            if reply != QMessageBox.Yes:
                event.ignore()
                return
            self.downloader.stop()
            self.downloader.wait(4000)
        if self.fetcher and self.fetcher.isRunning():
            self.fetcher.requestInterruption()
            self.fetcher.wait(2000)
        self._save_settings()
        event.accept()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QFont

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)

    default_font = QFont()
    default_font.setFamilies([
        "Leelawadee UI",
        "Kantumruy Pro",
        "Khmer OS Battambang",
        "Segoe UI",
        "Inter",
        "sans-serif",
    ])
    default_font.setPointSize(10)
    app.setFont(default_font)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())
