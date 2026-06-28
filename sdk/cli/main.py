"""
Atlas CLI — Main Entry Point
=============================

The official command-line interface for Atlas development.

Usage:
    atlas new worker my_worker
    atlas run
    atlas test
    atlas doctor
    atlas validate
    atlas inspect
    atlas info
    atlas clean
"""

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlas",
        description="Atlas CLI — The official developer interface for the Atlas Software Platform.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- atlas new ---
    new_parser = subparsers.add_parser("new", help="Scaffold a new Atlas project")
    new_parser.add_argument(
        "type",
        choices=["worker", "model", "adapter", "product"],
        help="Type of project to create",
    )
    new_parser.add_argument("name", help="Name of the project")
    new_parser.add_argument(
        "--template", default=None, help="Template variant to use"
    )

    # --- atlas run ---
    run_parser = subparsers.add_parser("run", help="Run the Atlas application")
    run_parser.add_argument(
        "--manifest", default="manifest.yaml", help="Path to the manifest file"
    )

    # --- atlas test ---
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument(
        "--generate", action="store_true", help="Generate test stubs from manifests"
    )

    # --- atlas doctor ---
    subparsers.add_parser("doctor", help="Validate your development environment")

    # --- atlas validate ---
    validate_parser = subparsers.add_parser("validate", help="Validate manifests")
    validate_parser.add_argument(
        "--manifest", default="manifest.yaml", help="Path to manifest"
    )

    # --- atlas inspect ---
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a Worker or Product")
    inspect_parser.add_argument(
        "--manifest", default="manifest.yaml", help="Path to manifest"
    )

    # --- atlas info ---
    subparsers.add_parser("info", help="Show Atlas SDK info")

    # --- atlas clean ---
    subparsers.add_parser("clean", help="Clean build artifacts")

    # --- atlas build ---
    build_parser = subparsers.add_parser("build", help="Build an .atlas package")
    build_parser.add_argument(
        "--output", default="dist", help="Output directory"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Import and dispatch to the appropriate command handler
    if args.command == "new":
        from .commands.new import handle_new
        handle_new(args)
    elif args.command == "run":
        from .commands.run import handle_run
        handle_run(args)
    elif args.command == "test":
        from .commands.test import handle_test
        handle_test(args)
    elif args.command == "doctor":
        from .commands.doctor import handle_doctor
        handle_doctor(args)
    elif args.command == "validate":
        from .commands.validate import handle_validate
        handle_validate(args)
    elif args.command == "inspect":
        from .commands.inspect import handle_inspect
        handle_inspect(args)
    elif args.command == "info":
        from .commands.info import handle_info
        handle_info(args)
    elif args.command == "clean":
        from .commands.clean import handle_clean
        handle_clean(args)
    elif args.command == "build":
        from .commands.build import handle_build
        handle_build(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
