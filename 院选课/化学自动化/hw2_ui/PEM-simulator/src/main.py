# src/main.py
import sys
import logging
import argparse
from PySide6.QtWidgets import QApplication

# Allow imports from src directory
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main_window import MainWindow
from widgets.fluent_compat import apply_app_theme


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="PEM Electrolysis Simulation")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    setup_logging(args.debug)

    app = QApplication(sys.argv)

    # Apply Fluent theme (falls back to Fusion if unavailable)
    apply_app_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
