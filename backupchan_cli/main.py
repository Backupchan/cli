from .commands import config, target
from .config import Config, ConfigException
from .utility import failure, NO_CONFIG_MESSAGE
from backupchan import API
import argparse

def main():
    parser = argparse.ArgumentParser(prog="backupchan")
    subparsers = parser.add_subparsers(dest="command")

    config_parser = subparsers.add_parser("config")
    config_sub = config_parser.add_subparsers(dest="subcommand", help="Commands for viewing and editing configuration")
    config.setup_subcommands(config_sub)

    target_parser = subparsers.add_parser("target")
    target_sub = target_parser.add_subparsers(dest="subcommand", help="Commands for viewing and managing targets")
    target.setup_subcommands(target_sub)

    app_config = Config()
    try:
        app_config.read_config()
    except ConfigException:
        app_config.reset()
        pass

    api = None if app_config.is_incomplete() else API(app_config.host, app_config.port, app_config.api_key)

    args = parser.parse_args()
    if hasattr(args, "func"):
        if args.command != "config" and app_config.is_incomplete():
            failure(NO_CONFIG_MESSAGE)

        args.func(args, app_config, api)
    else:
        parser.print_help()

    return 0
