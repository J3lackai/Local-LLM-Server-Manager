from loguru import logger
from llm_model import LLMModel
from llm_server import LLMServerRunner
from keyboard import wait
from time import sleep


def beautiful_exit():
    logger.info("Нажмите 'Enter' для завершения программы.")
    wait("enter")
    exit()


def wait_for_input(names_llm):
    try:
        logger.info(
            "Введите название модели LLM для запуска\nЗапуск дефолтной модели через 15 сек..."
        )
        for i in range(int(15), -1, -1):
            if i > 0:
                logger.info(f"Осталось секунд: {i}")  # Пишет в лог без блокировки ввода
            cmd = input(">>> ").strip().lower()
            if cmd in names_llm:
                return cmd
            sleep(5)
    except KeyboardInterrupt:
        beautiful_exit()


def cli(runner: LLMServerRunner, names_llm, dict_cmds, dict_llm) -> None:
    try:
        while True:
            cmd = input(">>> ").strip().lower()
            if cmd == runner.strategy.name:
                logger.info("Модель уже загружена")
                continue
            if cmd == "exit":
                runner.stop_server()
                beautiful_exit()
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
                    logger.error(f"Неизвестная языковая модель\nДоступные: {names_llm}")
                else:
                    runner.set_strategy(LLMModel(cmd, dict_llm))
                    runner.restart_server()
    except KeyboardInterrupt:
        runner.stop_server()
        beautiful_exit()
