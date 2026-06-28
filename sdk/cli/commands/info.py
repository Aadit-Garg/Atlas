"""
atlas info — Show Atlas SDK information.
"""


def handle_info(args):
    try:
        from atlas_sdk import __version__ as sdk_version
    except ImportError:
        sdk_version = "not installed"

    print("ℹ️  Atlas SDK Info\n")
    print(f"   SDK Version:     {sdk_version}")
    print(f"   Runtime:         Atlas Runtime v1 (frozen)")
    print(f"   Architecture:    v1.0 (frozen)")
    print(f"   First Language:  Python")
    print()
    print("   Primitives:      Worker, Room, Session, Registry, Binding, Invocation")
    print("   Studio Suite:    Miron (console), Solon (validator), Varsity (learning)")
    print()
    print("   📖 Docs: https://atlas-system-suite.github.io/Atlas/")
    print("   🐙 Repo: https://github.com/atlas-system-suite/Atlas")
