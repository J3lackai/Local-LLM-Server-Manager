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
    llama_path, llama_flags, default_llm, names_llm, dict_llm, dict_cmds = (
        get_config_data("config.ini", "utf-8")
    )
    psswrd = get_env_data()

    strategy = LLMModel(default_llm, dict_llm)
    server_data = ServerData(llama_path, llama_flags)

    runner = LLMServerRunner(strategy, server_data, psswrd)

    runner.start_server()

    while True:
        cmd = input(">>> ").strip().lower()
        if cmd == runner.strategy.name:
            logger.info("Модель уже загружена 😊")
            continue
        if cmd == "exit":
            runner.stop_server()
            break
        elif cmd == "help":
            for command, description in dict_cmds.items():
                logger.info(f"{command:15} - {description}")
        elif cmd == "list":
            logger.info(f"Доступные модели: {names_llm}")
        elif cmd == "info":
            logger.info(f"Текущая модель: {runner.strategy.get_name()}")
        else:
            if cmd not in names_llm:
                logger.error(
                    f"Неизвестная языковая модель😔\nДоступные: {runner.strategy.get_name()}"
                )
            else:
                runner.set_strategy(LLMModel(cmd, dict_llm))
                runner.restart_server()
    beautiful_exit()
