from llm_model import LLMModel
from load_data import get_config_data, get_env_data
from llm_server import LLMServerRunner, ServerData
from loguru import logger
from keyboard import wait


def beautiful_exit():
    logger.info("Нажмите 'Enter' для завершения программы.")
    wait("enter")
    exit()


if __name__ == "__main__":
    llama_path, llama_flags, default_llm, names_llm, dict_llm = get_config_data(
        "config.ini", "utf-8"
    )
    psswrd = get_env_data()

    strategy = LLMModel(default_llm, dict_llm)
    server_data = ServerData(llama_path, llama_flags)

    runner = LLMServerRunner(strategy, server_data, psswrd)

    runner.start_server()

    while True:
        cmd = input(">>> ").strip().lower()

        if cmd == "exit":
            runner.stop_server()
            break
        else:
            if cmd not in names_llm:
                logger.error("Unknown LLM name")
            else:
                runner.set_strategy(LLMModel(cmd, dict_llm))
                runner.restart_server()
    beautiful_exit()
