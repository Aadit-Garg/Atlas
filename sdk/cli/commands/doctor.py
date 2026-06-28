"""
atlas doctor — Validate the development environment.
"""

import sys
import os
import importlib


def handle_doctor(args):
    print("🩺 Atlas Doctor — Checking your environment...\n")

    issues = 0

    # 1. Python version
    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 13:
        print(f"   ✅ Python {major}.{minor} (>= 3.13 required)")
    else:
        print(f"   ❌ Python {major}.{minor} — Atlas requires >= 3.13")
        issues += 1

    # 2. PyYAML
    try:
        import yaml
        print(f"   ✅ PyYAML {yaml.__version__}")
    except ImportError:
        print("   ❌ PyYAML not installed (pip install pyyaml)")
        issues += 1

    # 3. Pydantic
    try:
        import pydantic
        print(f"   ✅ Pydantic {pydantic.__version__}")
    except ImportError:
        print("   ❌ Pydantic not installed (pip install pydantic)")
        issues += 1

    # 4. pytest
    try:
        import pytest
        print(f"   ✅ pytest {pytest.__version__}")
    except ImportError:
        print("   ⚠️  pytest not installed (pip install pytest)")

    # 5. Atlas SDK
    try:
        import atlas_sdk
        print(f"   ✅ Atlas SDK {atlas_sdk.__version__}")
    except ImportError:
        print("   ⚠️  Atlas SDK not on PYTHONPATH")

    # 6. Atlas Runtime
    try:
        from atlas.core.runtime import AtlasRuntime
        print("   ✅ Atlas Runtime found")
    except ImportError:
        print("   ⚠️  Atlas Runtime not on PYTHONPATH (optional for SDK-only development)")

    # 7. Manifest check
    if os.path.exists("manifest.yaml"):
        print("   ✅ manifest.yaml found in current directory")
    elif os.path.exists("product.yaml"):
        print("   ✅ product.yaml found in current directory")
    else:
        print("   ℹ️  No manifest found (run `atlas new worker my_worker` to get started)")

    print()
    if issues == 0:
        print("🎉 All checks passed! Your environment is ready for Atlas development.")
    else:
        print(f"⚠️  {issues} issue(s) found. Please fix them before continuing.")
