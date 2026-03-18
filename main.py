from llm_model import LLMModel
from utils import get_config_data, get_env_data, add_logger
from llm_server import LLMServerRunner, ServerData
from loguru import logger
from CLI import cli, wait_for_input

if __name__ == "__main__":
    # Убираем дефолтный логгер
    logger.remove()
    add_logger()
    # Настраиваем компактный формат

    llama_path, llama_flags, default_llm, names_llm, dict_llm, dict_cmds = (
        get_config_data("config.ini", "utf-8")
    )
    psswrd = get_env_data()
    cmd = wait_for_input(names_llm)
    strategy = LLMModel(default_llm if (cmd not in names_llm) else cmd, dict_llm)
    server_data = ServerData(llama_path, llama_flags)
    runner = LLMServerRunner(strategy, server_data, psswrd)
    runner.start_server()
    cli(runner, names_llm, dict_cmds, dict_llm)
