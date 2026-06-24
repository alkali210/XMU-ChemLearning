"""
Environment precheck script for PySide6-Fluent-Widgets.

Validates:
1. qfluentwidgets can be imported
2. Only one Fluent variant is present in environment

Exits with:
- 0: Environment is valid
- 1: Missing qfluentwidgets or multiple Fluent variants detected
"""

import sys
from importlib.metadata import distributions


def main() -> int:
    """Check Fluent environment and return exit code."""
    # Known Fluent widget package variants
    fluent_packages = {
        "PySide6-Fluent-Widgets",
        "PyQt5-Fluent-Widgets",
        "PyQt6-Fluent-Widgets",
    }

    # Find installed Fluent variants
    installed_fluent: set[str] = set()
    for dist in distributions():
        if dist.name in fluent_packages:
            installed_fluent.add(dist.name)

    # Check: at least one Fluent variant present
    if not installed_fluent:
        print("ERROR: No Fluent variant found.")
        print("Expected one of:")
        for pkg in sorted(fluent_packages):
            print(f"  - {pkg}")
        print("\nInstall with: pip install PySide6-Fluent-Widgets")
        return 1

    # Check: exactly one Fluent variant present
    if len(installed_fluent) > 1:
        print("ERROR: Multiple Fluent variants detected (conflict):")
        for pkg in sorted(installed_fluent):
            print(f"  - {pkg}")
        print("\nRemove conflicting packages and keep only one variant.")
        return 1

    # Check: qfluentwidgets can be imported
    try:
        import qfluentwidgets  # noqa: F401

        pkg_name = installed_fluent.pop()
        print(f"Environment valid: {pkg_name} installed and importable")
        return 0
    except ImportError as e:
        print(f"ERROR: qfluentwidgets import failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
