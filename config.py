from constants import Constants
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.__config = self.__load_config()

    def __load_config(self):
        config_path = Path(Constants.APP_CONFIG_FILE_PATH)
        if config_path.exists():
            with open(str(config_path)) as f:
                return(json.load(f))
        return {}

    def get(self, key:str, default=None):
        return self.__config.get(key, default)