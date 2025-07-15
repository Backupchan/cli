# Backup-chan CLI

This is the command-line interface program for interacting with a Backup-chan server.

## Installing

```bash
pip install .
```

You can also run right from source if you don't feel like installing the program:

```bash
./cli.py
```

## Configuring

The CLI has to first be configured before you can use it. Run:

```bash
# Interactive configuration.
backupchan config new -i

# Non-interactive configuration.
backupchan config new -H "http://host" -p 5050 -a "your api key"
```

Run `backupchan --help` to see all the commands you can use.
