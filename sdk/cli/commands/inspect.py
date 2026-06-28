"""
atlas inspect — Inspect an Atlas Worker or Product.
"""

import yaml
import os
import sys


def handle_inspect(args):
    manifest_path = args.manifest

    if not os.path.exists(manifest_path):
        print(f"❌ Manifest not found: {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r") as f:
        manifest = yaml.safe_load(f)

    print("🔎 Atlas Inspector\n")
    print(f"   ID:       {manifest.get('id', 'N/A')}")
    print(f"   Name:     {manifest.get('name', 'N/A')}")
    print(f"   Version:  {manifest.get('version', 'N/A')}")
    print(f"   Language:  {manifest.get('language', 'N/A')}")
    print(f"   Roles:     {', '.join(manifest.get('roles', []))}")

    execution = manifest.get("execution", {})
    print(f"   Policy:    {execution.get('policy', 'N/A')}")
    print()

    exports = manifest.get("exports", [])
    if exports:
        print("   📤 Exported Capabilities:")
        for e in exports:
            if isinstance(e, dict):
                print(f"      - {e.get('capability', '?')} v{e.get('version', '?')}")
            else:
                print(f"      - {e}")

    imports = manifest.get("imports", [])
    if imports:
        print("   📥 Required Capabilities:")
        for i in imports:
            if isinstance(i, dict):
                print(f"      - {i.get('capability', '?')}")
            else:
                print(f"      - {i}")

    translations = manifest.get("translations", [])
    if translations:
        print("   🔄 Translations:")
        for t in translations:
            if isinstance(t, dict):
                print(f"      - {t.get('source_format', '?')} → {t.get('target_format', '?')} (cost: {t.get('cost', '?')})")

    if not exports and not imports and not translations:
        print("   ℹ️  No capabilities, imports, or translations declared.")
