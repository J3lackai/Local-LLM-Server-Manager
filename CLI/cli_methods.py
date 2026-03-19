from loguru import logger
from llm_model import LLMModel
from keyboard import wait
import msvcrt
import time as t
import sys


def beautiful_exit():
    logger.info("Нажмите 'Enter' для завершения программы.")
    wait("enter")
    exit()


def input_with_timeout(
    prompt: str,
    timeout: float,
    names_llm: str,
    log_delay=5,
    timer=t.monotonic,
):
    logger.info(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    i = 0
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche())
            if result[-1] == "\r":
                cmd = "".join(result[:-1])
                if cmd in names_llm:
                    return cmd
                cmd = ""
                logger.error(
                    f"Неизвестная языковая модель: {cmd} Доступные: {names_llm}"
                )

        t.sleep(0.04)  # just to yield to other processes/threads
        if i % (24 * log_delay) == 0:
            # i % 24 Приблизительно 1 секунда задержки на вывод следующего сообщения
            logger.info(f"Осталось времени: {int(endtime - timer())}")
        i += 1


def cli(runner, names_llm, dict_cmds, dict_llm) -> None:
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
        logger.info("Программа завершена вводом: Ctrl + C")
        beautiful_exit()
