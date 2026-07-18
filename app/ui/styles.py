from __future__ import annotations

LIGHT = """
QWidget { background: #f6f7fb; color: #18202d; font-family: 'Segoe UI'; font-size: 14px; }
QFrame#sidebar { background: #162033; border: none; }
QFrame#sidebar QLabel { color: #f5f7fb; background: transparent; }
QPushButton#navButton { text-align: left; padding: 11px 16px; color: #dce4f2; background: transparent; border: none; border-radius: 7px; }
QPushButton#navButton:hover { background: #24334e; }
QPushButton#navButton:checked { background: #2e6ee6; color: white; font-weight: 600; }
QPushButton#primary { background: #2e6ee6; color: white; border: none; border-radius: 7px; padding: 9px 18px; font-weight: 600; }
QPushButton#primary:hover { background: #245dc5; }
QPushButton { padding: 8px 13px; border: 1px solid #cdd5e2; border-radius: 7px; background: white; }
QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox { background: white; border: 1px solid #cbd4e1; border-radius: 6px; padding: 7px; }
QLineEdit:focus, QTextEdit:focus { border: 2px solid #2e6ee6; }
QTableWidget { background: white; border: 1px solid #dbe1ea; border-radius: 8px; gridline-color: #edf0f5; }
QHeaderView::section { background: #eef2f8; padding: 8px; border: none; border-bottom: 1px solid #dbe1ea; font-weight: 600; }
QFrame#card { background: white; border: 1px solid #e0e5ed; border-radius: 10px; }
QStatusBar { background: white; border-top: 1px solid #e0e5ed; }
"""

DARK = """
QWidget { background: #111722; color: #e8edf5; font-family: 'Segoe UI'; font-size: 14px; }
QFrame#sidebar { background: #0b1019; border: none; }
QFrame#sidebar QLabel { color: #f5f7fb; background: transparent; }
QPushButton#navButton { text-align: left; padding: 11px 16px; color: #cdd7e8; background: transparent; border: none; border-radius: 7px; }
QPushButton#navButton:hover { background: #202b3e; }
QPushButton#navButton:checked { background: #397cf0; color: white; font-weight: 600; }
QPushButton#primary { background: #397cf0; color: white; border: none; border-radius: 7px; padding: 9px 18px; font-weight: 600; }
QPushButton#primary:hover { background: #4c8af4; }
QPushButton { padding: 8px 13px; border: 1px solid #3a4658; border-radius: 7px; background: #202938; }
QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox { background: #192231; border: 1px solid #3a4658; border-radius: 6px; padding: 7px; }
QTableWidget { background: #192231; border: 1px solid #354154; border-radius: 8px; gridline-color: #2b3545; }
QHeaderView::section { background: #202b3a; padding: 8px; border: none; border-bottom: 1px solid #354154; font-weight: 600; }
QFrame#card { background: #192231; border: 1px solid #303c4f; border-radius: 10px; }
QStatusBar { background: #151d29; border-top: 1px solid #303c4f; }
"""
