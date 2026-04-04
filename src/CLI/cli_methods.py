from loguru import logger
from llm_model import LLMModel
from keyboard import wait
import sys
from input_with_timeout import input_with_timeout
from utils import CLISettings


def beautiful_exit():
    logger.info("Нажмите 'Enter' для завершения программы.")
    wait("enter")
    sys.exit()


def input_llm_name_timeout(prompt: str, timeout: float, cli_s: CLISettings):
    if cli_s is None:
        logger.critical("Ошибка: cli_s не может быть None")
        raise (TimeoutError)
    try:
        cancel = {"no", "none", "n"}
        cmd = input_with_timeout(prompt, timeout)
        if cmd.lower() in cancel:
            return "n"
        if cmd not in cli_s.names_llm:
            logger.warning(f"Модель {cmd} не найдена среди моделей: {cli_s.names_llm}")
            cmd = cli_s.default_llm
            logger.warning(f"Выбрана дефолтная модель: {cmd}")
            return cmd
    except TimeoutError:
        logger.warning("Вы не ввели название модели")
    except ValueError:
        logger.warning("Ошибка: timeout должен быть > 0")
    except TypeError:
        logger.warning("Ошибка: timeout должен быть одним из типов: int, float, None")
    cmd = cli_s.default_llm
    logger.warning(f"Выбрана дефолтная модель: {cmd}")
    return cmd


def cli(runner, names_llm, dict_cmds, dict_llm) -> None:
    try:
        # Реализация функции ввода команд в консоль
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
                    logger.error(f"Неизвестная LLM: {cmd}; Доступные: {names_llm}")
                else:
                    runner.set_strategy(LLMModel(cmd, dict_llm))
                    runner.restart_server()
    except KeyboardInterrupt:
        runner.stop_server()
        logger.info("Программа завершена вводом: Ctrl + C")
        beautiful_exit()
