import sys

NO_CONFIG_MESSAGE = "No configuration. Run `backupchan config new' to configure."

def is_parsable_int(number_str: str) -> bool:
    try:
        int(number_str)
        return True
    except ValueError:
        return False

def failure(message: str):
    print(f"{message}. Halting.", file=sys.stderr)
    sys.exit(1)

def failure_network():
    failure("Failed to connect to server")
