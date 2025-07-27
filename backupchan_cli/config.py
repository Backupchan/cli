import json
import sys
import platformdirs
import keyring
import os
from pathlib import Path

class ConfigException(Exception):
    pass

CONFIG_FILE_DIR = platformdirs.user_config_dir('backupchan')
CONFIG_FILE_PATH = f"{CONFIG_FILE_DIR}/config.json"

class Config:
    def __init__(self):
        self.port: int | None = None
        self.host: str | None = None
        self.api_key: str | None = None

    def read_config(self):
        if not os.path.exists(CONFIG_FILE_PATH):
            raise ConfigException("Config file not found")

        with open(CONFIG_FILE_PATH, "r") as config_file:
            self.parse_config(config_file.read())
        self.retrieve_api_key()

    def reset(self, write: bool = False):
        self.port = None
        self.host = None
        self.api_key = None

        if write:
            self.delete_api_key()
            if os.path.exists(CONFIG_FILE_PATH):
                os.remove(CONFIG_FILE_PATH)

    def is_incomplete(self):
        return self.port is None or self.host is None or self.api_key is None

    def parse_config(self, config: str):
        config_json = json.loads(config)
        self.port = config_json["port"]
        self.host = config_json["host"]

    def retrieve_api_key(self):
        self.api_key = keyring.get_password("backupchan", "api_key")

    def save_config(self):
        if self.is_incomplete():
            raise ConfigException("Cannot save incomplete config")
        
        Path(CONFIG_FILE_DIR).mkdir(exist_ok=True, parents=True)

        config_dict = {
            "host": self.host,
            "port": self.port
        }

        with open(CONFIG_FILE_PATH, "w") as config_file:
            json.dump(config_dict, config_file)

        self.save_api_key()

    def delete_api_key(self):
        try:
            keyring.delete_password("backupchan", "api_key")
        except keyring.errors.PasswordDeleteError:
            pass
    
    def save_api_key(self):
        keyring.set_password("backupchan", "api_key", self.api_key)
