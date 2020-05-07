import json
import copy
from json import load
from os import path, sys
from singleton_type import SingletonType


####################################################################
#       CONFIGURATION                                              #
####################################################################
# I need to check if the application is running as a script or
# as an exe for get the right path
BASE_PATH = ""
if getattr(sys, 'frozen', False):
    BASE_PATH = path.dirname(sys.executable)
elif __file__:
    BASE_PATH = path.dirname(__file__)
JSON_CONFIG_FILE = path.join(BASE_PATH, "digiSign_config.json")
####################################################################


class MyConfigLoader(object, metaclass=SingletonType):
    _config = None

    def __init__(self):
        config_modified = False
        default_config = None
        with open(JSON_CONFIG_FILE) as _file:
            self._config = load(_file)
            default_config = copy.deepcopy(self._config)
        # adding BASE_PATH to all folder names
        for group in self._config:
            if group == "server" and "enable_proxy" not in self._config[group]:
                default_config[group]["enable_proxy"] = False
                self._config[group]["enable_proxy"] = False
                config_modified = True
            for item in self._config[group]:
                if item.find("_folder") >= 0:
                    folder_name = self._config[group][item]
                    self._config[group][item] = path.join(
                        BASE_PATH, folder_name)
        if config_modified is True:
            with open(JSON_CONFIG_FILE, 'w') as _file:
                _file.write(json.dumps(default_config, indent=4))

    def get_logger_config(self):
        return self._config["logger"]

    def get_server_config(self):
        return self._config["server"]

    def get_pdf_config(self):
        return self._config["pdf_conf"]

    def get_rev_checker_apis(self):
        return self._config["rev_checker_apis"]
