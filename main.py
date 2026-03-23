from llm_model import LLMModel
from utils import get_config_data, get_env_data, add_logger
from llm_server import LLMServerRunner, ServerData
from loguru import logger
from CLI import cli, input_llm_name_timeout, beautiful_exit

if __name__ == "__main__":
    try:
        # Убираем дефолтный логгер
        logger.remove()
        add_logger()
        # Настраиваем компактный формат

        cmd_p, cli_s, llm_s = get_config_data("config.ini", "utf-8")
        psswrd = get_env_data()
        prompt = (
            f"Напишите название LLM для запуска, Осталось {cli_s.timeout} секунд.\n>>"
        )
        cmd = input_llm_name_timeout(prompt, cli_s.timeout, cli_s)
        if cmd is None:
            logger.critical("Ошибка во время выполнения input_with_timeout")
        strategy = LLMModel(cmd, llm_s.dict_llm)
        server_data = ServerData(cmd_p.llama_path, cmd_p.llama_flags, cmd_p.backend)
        runner = LLMServerRunner(strategy, server_data, psswrd)
        runner.start_server()
        cli(runner, cli_s.names_llm, cli_s.dict_cmds, llm_s.dict_llm)
    except ModuleNotFoundError as e:
        print(f"Не смогли загрузить библиотеки: {e}")
        beautiful_exit()
    except KeyboardInterrupt:
        logger.info("Программа завершена вводом: Ctrl + C")
        beautiful_exit()
    except WindowsError as e:
        logger.critical(f"Ошибка: {e}")
        beautiful_exit()
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        beautiful_exit()
