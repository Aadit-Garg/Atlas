from sdk.atlas_sdk.discovery import DiscoveryEngine
import argparse
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class StudioCliWorker:
    def __init__(self):
        self.atlas_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.engine = DiscoveryEngine(self.atlas_root)

    def _create_parser(self):
        parser = argparse.ArgumentParser(
            prog="atlas studio",
            description="Atlas Studio — Workspace Manager & Development Hub",
        )
        subparsers = parser.add_subparsers(dest="group", help="Command groups")

        # Managers
        managers_parser = subparsers.add_parser("managers", help="Manage installed managers")
        managers_sub = managers_parser.add_subparsers(dest="subcommand")
        managers_sub.add_parser("list", help="List all installed managers")
        managers_sub.add_parser("show", help="Show manager details").add_argument("name")
        managers_sub.add_parser("launch", help="Launch a manager").add_argument("name")

        # Workers
        workers_parser = subparsers.add_parser("workers", help="Manage installed workers")
        workers_sub = workers_parser.add_subparsers(dest="subcommand")
        workers_sub.add_parser("list", help="List all installed workers")
        workers_sub.add_parser("show", help="Show worker details").add_argument("name")
        
        # Projects, Models, Packages, Workspace, Docs, Examples, Settings
        for group in ["projects", "models", "packages", "workspace", "docs", "examples", "settings"]:
            grp = subparsers.add_parser(group, help=f"Manage {group}")
            grp_sub = grp.add_subparsers(dest="subcommand")
            grp_sub.add_parser("list", help=f"List {group}")

        return parser

    def handle_managers(self, args):
        if args.subcommand == "list":
            table = Table(title="Installed Atlas Managers", header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Name")
            table.add_column("Version")
            table.add_column("Description")
            
            for mgr in self.engine.list_managers():
                data = mgr["manifest"]
                table.add_row(
                    data.get("id", "N/A"),
                    data.get("name", "N/A"),
                    str(data.get("version", "N/A")),
                    data.get("description", "")
                )
            console.print(table)
        else:
            console.print(f"[yellow]Command 'managers {args.subcommand}' is under construction.[/yellow]")

    def handle_workers(self, args):
        if args.subcommand == "list":
            table = Table(title="Installed Atlas Workers", header_style="bold green")
            table.add_column("ID", style="cyan")
            table.add_column("Name")
            table.add_column("Version")
            table.add_column("Description")
            
            for wkr in self.engine.list_workers():
                data = wkr["manifest"]
                table.add_row(
                    data.get("id", "N/A"),
                    data.get("name", "N/A"),
                    str(data.get("version", "N/A")),
                    data.get("description", "")
                )
            console.print(table)
        else:
            console.print(f"[yellow]Command 'workers {args.subcommand}' is under construction.[/yellow]")

    def on_invoke(self, capability: str, args: dict):
        if capability == "studio.cli.execute":
            cli_args = args.get("args", [])
            if not cli_args:
                # Fallback to TUI
                self.on_invoke("studio.tui.launch", {})
                return {"status": "ok"}

            parser = self._create_parser()
            parsed_args = parser.parse_args(cli_args)

            if parsed_args.group == "managers":
                self.handle_managers(parsed_args)
            elif parsed_args.group == "workers":
                self.handle_workers(parsed_args)
            elif parsed_args.group:
                console.print(f"[yellow]Group '{parsed_args.group}' is recognized but under construction.[/yellow]")
            else:
                parser.print_help()

            return {"status": "ok"}
            
        elif capability == "studio.tui.launch":
            console.print(Panel(
                "[bold cyan]Welcome to Atlas Studio[/bold cyan]\n\n"
                "To get started, try the following commands:\n"
                "  [green]atlas studio managers list[/green]\n"
                "  [green]atlas studio workers list[/green]\n"
                "  [green]atlas studio projects[/green]\n\n"
                "Miron (Runtime console) integration pending.",
                title="Atlas Studio Suite",
                border_style="blue"
            ))
            return {"status": "ok"}

# Module-level entry point
_instance = StudioCliWorker()

def on_invoke(capability: str, args: dict):
    return _instance.on_invoke(capability, args)
