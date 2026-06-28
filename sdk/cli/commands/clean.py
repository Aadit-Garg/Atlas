"""
atlas clean — Clean build artifacts.
"""

import os
import shutil


CLEAN_DIRS = ["dist", "__pycache__", ".pytest_cache", "build", ".atlas_cache"]
CLEAN_PATTERNS = [".pyc", ".pyo"]


def handle_clean(args):
    print("🧹 Cleaning build artifacts...\n")

    removed = 0
    for dirname in CLEAN_DIRS:
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
            print(f"   🗑️  Removed {dirname}/")
            removed += 1

    # Walk current directory for __pycache__ dirs
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                path = os.path.join(root, d)
                shutil.rmtree(path)
                print(f"   🗑️  Removed {path}")
                removed += 1

    if removed == 0:
        print("   ✨ Nothing to clean!")
    else:
        print(f"\n   Cleaned {removed} artifact(s).")
