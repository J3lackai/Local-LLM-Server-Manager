import os
from configparser import ConfigParser


def get_name_llm(llm_path: str) -> str:
    list_llm_path = llm_path.split("\\")
    return list_llm_path[-2] if len(list_llm_path) >= 2 else ""


def get_config_data(
    path="config.ini",
    encoding="utf-8",
    suffixes=("_flags", "_path"),
) -> tuple[str, str, dict[str, str]]:
    config = ConfigParser()
    config.read(path, encoding)

    config_main = config["Main"]
    llama_flags = config_main["flags"]
    llama_path = config_main["server_path"]

    dict_llm = {}

    for key, value in config_main.items():
        for suffix in suffixes:
            if key.endswith(suffix):
                dict_llm[key] = value

    return llama_path, llama_flags, dict_llm


def get_env_data() -> str:
    return os.environ["psswrd"] if os.environ["psswrd"] else ""
