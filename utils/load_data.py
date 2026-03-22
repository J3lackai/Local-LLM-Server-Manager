import os
import ast
from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class CLISettings:
    timeout: int
    names_llm: tuple
    dict_cmds: dict
    default_llm: str


@dataclass
class CMDParameters:
    backend: str
    llama_path: str
    llama_flags: str


@dataclass
class LLMSettings:
    dict_llm: dict


def get_name_llm(llm_path: str) -> str:
    list_llm_path = llm_path.split("\\")
    return list_llm_path[-2] if len(list_llm_path) >= 2 else ""


def get_config_data(
    path="config.ini",
    encoding="utf-8",
) -> tuple[CMDParameters, CLISettings, LLMSettings]:
    config = ConfigParser()
    config.read(path, encoding)

    config_main = config["Main"]
    server_path = config_main["server_path"]
    if not os.path.exists(server_path):
        raise FileNotFoundError("llama-server.exe не найден")
    cmd_p = CMDParameters(
        llama_path=server_path,
        llama_flags=config_main["flags"],
        backend=config_main["backend"],
    )
    names_llm = tuple(
        (config_main["llm_list"])
        .replace("[", "")
        .replace("]", "")
        .replace(" ", "")
        .split(",")
    )
    dict_cmds = ast.literal_eval(config_main["dict_cmds"])
    cli_s = CLISettings(
        timeout=float(config_main["timeout"]),
        names_llm=names_llm,
        dict_cmds=dict_cmds,
        default_llm=config_main["default_llm"],
    )
    dict_llm = {}
    for section in config.sections():
        if section == "Main":
            continue
        for key, value in config[section].items():
            dict_key = section + "_" + key
            dict_llm[dict_key] = value
    llm_s = LLMSettings(dict_llm)
    return cmd_p, cli_s, llm_s


def get_env_data() -> str:
    return os.environ["psswrd"] if os.environ["psswrd"] else ""
