import os
import ast
from configparser import ConfigParser


def get_name_llm(llm_path: str) -> str:
    list_llm_path = llm_path.split("\\")
    return list_llm_path[-2] if len(list_llm_path) >= 2 else ""


def get_config_data(
    path="config.ini",
    encoding="utf-8",
) -> tuple[str, str, dict[str, str]]:
    config = ConfigParser()
    config.read(path, encoding)

    config_main = config["Main"]
    default_llm = config_main["default_llm"]
    llama_flags = config_main["flags"]
    llama_path = config_main["server_path"]
    names_llm = config_main["llm_list"]
    dict_cmds = ast.literal_eval(config_main["dict_cmds"])
    dict_llm = {}
    for section in config.sections():
        if section == "Main":
            continue
        for key, value in config[section].items():
            dict_key = section + "_" + key
            dict_llm[dict_key] = value

    return llama_path, llama_flags, default_llm, names_llm, dict_llm, dict_cmds


def get_env_data() -> str:
    return os.environ["psswrd"] if os.environ["psswrd"] else ""
