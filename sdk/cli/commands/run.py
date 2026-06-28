"""
atlas run — Run an Atlas application.
"""

import yaml
import os
import sys


def handle_run(args):
    manifest_path = args.manifest

    if not os.path.exists(manifest_path):
        print(f"❌ Manifest not found: {manifest_path}")
        print("   Are you in an Atlas project directory?")
        sys.exit(1)

    with open(manifest_path, "r") as f:
        manifest = yaml.safe_load(f)

    worker_name = manifest.get("name", manifest.get("id", "Unknown"))
    print(f"🚀 Atlas Runtime — Starting '{worker_name}'")
    print(f"   Manifest: {manifest_path}")
    print(f"   Language: {manifest.get('language', 'python')}")
    print(f"   Policy:   {manifest.get('execution', {}).get('policy', 'singleton')}")
    print()

    # For now, we print the manifest summary.
    # Full runtime boot integration comes in a later sprint.
    exports = manifest.get("exports", [])
    imports = manifest.get("imports", [])

    if exports:
        print("   📤 Exports:")
        for e in exports:
            cap = e.get("capability", e) if isinstance(e, dict) else e
            print(f"      - {cap}")

    if imports:
        print("   📥 Imports:")
        for i in imports:
            cap = i.get("capability", i) if isinstance(i, dict) else i
            print(f"      - {cap}")

    print()
    print("   ✅ Worker loaded successfully.")
    print("   ℹ️  Full runtime integration coming in Phase 2.")
