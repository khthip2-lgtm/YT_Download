"""Modern, premium Dark and Light stylesheets for YouTube Downloader with optimized Khmer typography."""

DARK_STYLESHEET = """
/* =========================================================================
   Global Root & Typography (DARK THEME)
   ========================================================================= */
QWidget#Root {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #0B0F19,
        stop: 0.35 #111827,
        stop: 0.7 #162032,
        stop: 1 #0D131F
    );
}

QWidget {
    color: #E2E8F0;
    font-family: "Leelawadee UI", "Kantumruy Pro", "Khmer OS Battambang", "Khmer OS Content", "Noto Sans Khmer", "Segoe UI", "Inter", sans-serif;
    font-size: 14px;
    selection-background-color: #0284C7;
    selection-color: #FFFFFF;
}

/* Cards & Panels */
QFrame#OptionsCard {
    background-color: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}

/* Labels */
QLabel#AppTitle {
    color: #FFFFFF;
    font-weight: 800;
    font-size: 20px;
    letter-spacing: 0.5px;
}

QLabel#AppBadge {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EC4899, stop:1 #8B5CF6);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 11.5px;
    border-radius: 6px;
    padding: 2px 8px;
}

QLabel#SectionLabel {
    color: #94A3B8;
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Theme Toggle Button */
QPushButton#ThemeBtn {
    background: rgba(255, 255, 255, 0.07);
    color: #FBBF24;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    padding: 4px 14px;
    min-height: 24px;
}
QPushButton#ThemeBtn:hover {
    background: rgba(251, 191, 36, 0.15);
    border-color: #FBBF24;
    color: #FDE68A;
}
QPushButton#ThemeBtn:pressed {
    background: rgba(251, 191, 36, 0.25);
}

/* Inputs */
QLineEdit {
    background: rgba(15, 23, 42, 0.85);
    color: #F8FAFC;
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 14px;
}
QLineEdit:hover {
    border: 1.5px solid rgba(56, 189, 248, 0.5);
    background: rgba(15, 23, 42, 0.95);
}
QLineEdit:focus {
    border: 1.5px solid #38BDF8;
    background: #0F172A;
}

QLineEdit#UrlInput {
    font-size: 14.5px;
    padding: 8px 14px;
    border-radius: 10px;
    background: rgba(15, 23, 42, 0.9);
    border: 1.5px solid rgba(56, 189, 248, 0.35);
}
QLineEdit#UrlInput:focus {
    border: 1.5px solid #38BDF8;
    background: #0B1120;
}

/* Table */
QTableWidget {
    background: rgba(15, 23, 42, 0.75);
    color: #E2E8F0;
    font-size: 14px;
    gridline-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    outline: none;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
QTableWidget::item:selected {
    background-color: rgba(56, 189, 248, 0.2);
    color: #38BDF8;
}

QHeaderView::section {
    background: #0B1120;
    color: #94A3B8;
    font-weight: 700;
    font-size: 12.5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: none;
    border-bottom: 1.5px solid rgba(255, 255, 255, 0.08);
    border-right: 1px solid rgba(255, 255, 255, 0.04);
    padding: 8px 10px;
}

/* Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #2563EB);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 14px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    padding: 8px 16px;
    min-height: 22px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0EA5E9, stop:1 #3B82F6);
    border-color: rgba(255, 255, 255, 0.3);
}
QPushButton:disabled {
    background: rgba(30, 41, 59, 0.6);
    color: #64748B;
    border: 1px solid rgba(255, 255, 255, 0.04);
}

QPushButton#FetchBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F59E0B, stop:1 #EA580C);
    border-radius: 9px;
    font-size: 14.5px;
}
QPushButton#FetchBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FBBF24, stop:1 #F97316);
}

QPushButton#DownloadBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10B981, stop:1 #059669);
    border-radius: 9px;
    font-size: 14.5px;
}
QPushButton#DownloadBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34D399, stop:1 #10B981);
}

QPushButton#StopBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F43F5E, stop:1 #E11D48);
    border-radius: 9px;
    font-size: 14.5px;
}
QPushButton#StopBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FB7185, stop:1 #F43F5E);
}

QPushButton#ClearBtn {
    background: rgba(255, 255, 255, 0.05);
    color: #CBD5E1;
    font-weight: 600;
    font-size: 14px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 9px;
}
QPushButton#ClearBtn:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
    border-color: rgba(255, 255, 255, 0.25);
}

QPushButton#BrowseBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #0369A1);
    border-radius: 8px;
    font-size: 13.5px;
}
QPushButton#BrowseBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0EA5E9, stop:1 #0284C7);
}

QPushButton#OpenBtn {
    background: rgba(255, 255, 255, 0.06);
    color: #F1F5F9;
    font-weight: 600;
    font-size: 13.5px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 8px;
}
QPushButton#OpenBtn:hover {
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
    border-color: #38BDF8;
}

QPushButton#RowBtn {
    background: rgba(56, 189, 248, 0.12);
    color: #38BDF8;
    font-weight: 600;
    font-size: 13px;
    padding: 2px 10px;
    border: 1px solid rgba(56, 189, 248, 0.3);
    border-radius: 6px;
}
QPushButton#RowBtn:hover {
    background: #0284C7;
    color: #FFFFFF;
    border-color: #0284C7;
}

QPushButton#RowDanger {
    background: rgba(244, 63, 94, 0.12);
    color: #FB7185;
    font-weight: 700;
    font-size: 13px;
    border: 1px solid rgba(244, 63, 94, 0.3);
    border-radius: 6px;
    padding: 0;
}
QPushButton#RowDanger:hover {
    background: #E11D48;
    color: #FFFFFF;
    border-color: #E11D48;
}

/* ComboBox */
QComboBox {
    background: rgba(15, 23, 42, 0.85);
    color: #F8FAFC;
    border: 1.5px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 14px;
    min-height: 28px;
}
QComboBox:hover {
    border: 1.5px solid rgba(56, 189, 248, 0.5);
    background: rgba(15, 23, 42, 0.95);
}
QComboBox:focus {
    border: 1.5px solid #38BDF8;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid rgba(255, 255, 255, 0.08);
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background: rgba(30, 41, 59, 0.5);
}
QComboBox::down-arrow {
    width: 0px;
    height: 0px;
    border-left: 4.5px solid transparent;
    border-right: 4.5px solid transparent;
    border-top: 5px solid #94A3B8;
}
QComboBox QAbstractItemView {
    background: #0F172A;
    color: #F8FAFC;
    font-size: 14px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    selection-background-color: #0284C7;
    selection-color: #FFFFFF;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    min-height: 30px;
    padding: 4px 10px;
    border-radius: 6px;
}
QComboBox QAbstractItemView::item:hover {
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
}

/* Progress Bar */
QProgressBar {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 7px;
    text-align: center;
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 600;
    min-height: 20px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:0.5 #10B981, stop:1 #059669);
    border-radius: 6px;
}

/* Scrollbars */
QScrollBar:vertical {
    background: rgba(15, 23, 42, 0.5);
    width: 9px;
    margin: 0;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.16);
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(56, 189, 248, 0.5);
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}
QScrollBar:horizontal {
    background: rgba(15, 23, 42, 0.5);
    height: 9px;
    margin: 0;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 0.16);
    min-width: 24px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: rgba(56, 189, 248, 0.5);
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    width: 0px;
}

/* Status Bar & Tooltip */
QStatusBar {
    background: #080C14;
    color: #94A3B8;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    font-size: 13.5px;
    font-weight: 500;
    padding: 4px 8px;
}
QStatusBar QLabel { color: #94A3B8; font-size: 13.5px; }
QToolTip {
    background: #0F172A;
    color: #F8FAFC;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}

/* Dialogs */
QMessageBox, QDialog { background-color: #0F172A; }
QMessageBox QLabel, QDialog QLabel { color: #F8FAFC; font-size: 14.5px; }
QMessageBox QPushButton, QDialog QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #2563EB);
    color: #FFFFFF;
    font-weight: 600;
    font-size: 14px;
    border: none;
    border-radius: 7px;
    padding: 8px 20px;
    min-width: 85px;
    min-height: 24px;
}
"""

LIGHT_STYLESHEET = """
/* =========================================================================
   Global Root & Typography (LIGHT THEME)
   ========================================================================= */
QWidget#Root {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #F8FAFC,
        stop: 0.35 #F1F5F9,
        stop: 0.7 #E2E8F0,
        stop: 1 #CBD5E1
    );
}

QWidget {
    color: #0F172A;
    font-family: "Leelawadee UI", "Kantumruy Pro", "Khmer OS Battambang", "Khmer OS Content", "Noto Sans Khmer", "Segoe UI", "Inter", sans-serif;
    font-size: 14px;
    selection-background-color: #0284C7;
    selection-color: #FFFFFF;
}

/* Cards & Panels */
QFrame#OptionsCard {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
}

/* Labels */
QLabel#AppTitle {
    color: #0F172A;
    font-weight: 800;
    font-size: 20px;
    letter-spacing: 0.5px;
}

QLabel#AppBadge {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EC4899, stop:1 #8B5CF6);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 11.5px;
    border-radius: 6px;
    padding: 2px 8px;
}

QLabel#SectionLabel {
    color: #475569;
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Theme Toggle Button */
QPushButton#ThemeBtn {
    background: #FFFFFF;
    color: #4338CA;
    font-weight: 700;
    font-size: 13px;
    border: 1.5px solid #CBD5E1;
    border-radius: 15px;
    padding: 4px 14px;
    min-height: 24px;
}
QPushButton#ThemeBtn:hover {
    background: #EEF2FF;
    border-color: #6366F1;
    color: #3730A3;
}
QPushButton#ThemeBtn:pressed {
    background: #E0E7FF;
}

/* Inputs */
QLineEdit {
    background: #FFFFFF;
    color: #0F172A;
    border: 1.5px solid #CBD5E1;
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 14px;
}
QLineEdit:hover {
    border: 1.5px solid #94A3B8;
    background: #FFFFFF;
}
QLineEdit:focus {
    border: 1.5px solid #0284C7;
    background: #FFFFFF;
}

QLineEdit#UrlInput {
    font-size: 14.5px;
    padding: 8px 14px;
    border-radius: 10px;
    background: #FFFFFF;
    border: 1.5px solid #93C5FD;
}
QLineEdit#UrlInput:focus {
    border: 1.5px solid #0284C7;
}

/* Table */
QTableWidget {
    background: #FFFFFF;
    color: #0F172A;
    font-size: 14px;
    gridline-color: #E2E8F0;
    border: 1px solid #CBD5E1;
    border-radius: 10px;
    outline: none;
}
QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #F1F5F9;
}
QTableWidget::item:selected {
    background-color: #E0F2FE;
    color: #0369A1;
}

QHeaderView::section {
    background: #F1F5F9;
    color: #334155;
    font-weight: 700;
    font-size: 12.5px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: none;
    border-bottom: 1.5px solid #CBD5E1;
    border-right: 1px solid #E2E8F0;
    padding: 8px 10px;
}

/* Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #2563EB);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 14px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 8px;
    padding: 8px 16px;
    min-height: 22px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0EA5E9, stop:1 #3B82F6);
}
QPushButton:disabled {
    background: #E2E8F0;
    color: #94A3B8;
    border: 1px solid #CBD5E1;
}

QPushButton#FetchBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F59E0B, stop:1 #EA580C);
    border-radius: 9px;
    font-size: 14.5px;
}
QPushButton#FetchBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FBBF24, stop:1 #F97316);
}

QPushButton#DownloadBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10B981, stop:1 #059669);
    border-radius: 9px;
    font-size: 14.5px;
}
QPushButton#DownloadBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #34D399, stop:1 #10B981);
}

QPushButton#StopBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F43F5E, stop:1 #E11D48);
    border-radius: 9px;
    font-size: 14.5px;
}
QPushButton#StopBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FB7185, stop:1 #F43F5E);
}

QPushButton#ClearBtn {
    background: #F1F5F9;
    color: #334155;
    font-weight: 600;
    font-size: 14px;
    border: 1px solid #CBD5E1;
    border-radius: 9px;
}
QPushButton#ClearBtn:hover {
    background: #E2E8F0;
    color: #0F172A;
    border-color: #94A3B8;
}

QPushButton#BrowseBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #0369A1);
    border-radius: 8px;
    font-size: 13.5px;
}
QPushButton#BrowseBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0EA5E9, stop:1 #0284C7);
}

QPushButton#OpenBtn {
    background: #FFFFFF;
    color: #0F172A;
    font-weight: 600;
    font-size: 13.5px;
    border: 1.5px solid #CBD5E1;
    border-radius: 8px;
}
QPushButton#OpenBtn:hover {
    background: #F0F9FF;
    color: #0284C7;
    border-color: #0284C7;
}

QPushButton#RowBtn {
    background: #E0F2FE;
    color: #0284C7;
    font-weight: 600;
    font-size: 13px;
    padding: 2px 10px;
    border: 1px solid #BAE6FD;
    border-radius: 6px;
}
QPushButton#RowBtn:hover {
    background: #0284C7;
    color: #FFFFFF;
    border-color: #0284C7;
}

QPushButton#RowDanger {
    background: #FEE2E2;
    color: #E11D48;
    font-weight: 700;
    font-size: 13px;
    border: 1px solid #FECACA;
    border-radius: 6px;
    padding: 0;
}
QPushButton#RowDanger:hover {
    background: #E11D48;
    color: #FFFFFF;
    border-color: #E11D48;
}

/* ComboBox */
QComboBox {
    background: #FFFFFF;
    color: #0F172A;
    border: 1.5px solid #CBD5E1;
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 14px;
    min-height: 28px;
}
QComboBox:hover {
    border: 1.5px solid #94A3B8;
}
QComboBox:focus {
    border: 1.5px solid #0284C7;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #E2E8F0;
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
    background: #F8FAFC;
}
QComboBox::down-arrow {
    width: 0px;
    height: 0px;
    border-left: 4.5px solid transparent;
    border-right: 4.5px solid transparent;
    border-top: 5px solid #475569;
}
QComboBox QAbstractItemView {
    background: #FFFFFF;
    color: #0F172A;
    font-size: 14px;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    selection-background-color: #0284C7;
    selection-color: #FFFFFF;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    min-height: 30px;
    padding: 4px 10px;
    border-radius: 6px;
}
QComboBox QAbstractItemView::item:hover {
    background: #F0F9FF;
    color: #0284C7;
}

/* Progress Bar */
QProgressBar {
    background: #E2E8F0;
    border: 1px solid #CBD5E1;
    border-radius: 7px;
    text-align: center;
    color: #0F172A;
    font-size: 12px;
    font-weight: 600;
    min-height: 20px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06B6D4, stop:0.5 #10B981, stop:1 #059669);
    border-radius: 6px;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #F1F5F9;
    width: 9px;
    margin: 0;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #CBD5E1;
    min-height: 24px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #94A3B8;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}
QScrollBar:horizontal {
    background: #F1F5F9;
    height: 9px;
    margin: 0;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #CBD5E1;
    min-width: 24px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal:hover {
    background: #94A3B8;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    width: 0px;
}

/* Status Bar & Tooltip */
QStatusBar {
    background: #F8FAFC;
    color: #64748B;
    border-top: 1px solid #E2E8F0;
    font-size: 13.5px;
    font-weight: 500;
    padding: 4px 8px;
}
QStatusBar QLabel { color: #64748B; font-size: 13.5px; }
QToolTip {
    background: #0F172A;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}

/* Dialogs */
QMessageBox, QDialog { background-color: #FFFFFF; }
QMessageBox QLabel, QDialog QLabel { color: #0F172A; font-size: 14.5px; }
QMessageBox QPushButton, QDialog QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284C7, stop:1 #2563EB);
    color: #FFFFFF;
    font-weight: 600;
    font-size: 14px;
    border: none;
    border-radius: 7px;
    padding: 8px 20px;
    min-width: 85px;
    min-height: 24px;
}
"""


def get_stylesheet(theme: str = "dark") -> str:
    """Return the stylesheet corresponding to the given theme name ('dark' or 'light')."""
    return LIGHT_STYLESHEET if theme.lower() == "light" else DARK_STYLESHEET


STYLESHEET = DARK_STYLESHEET
