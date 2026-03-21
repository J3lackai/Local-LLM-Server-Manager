from llm_model import LLMModel
from utils import get_config_data, get_env_data, add_logger
from llm_server import LLMServerRunner, ServerData
from loguru import logger
from CLI import cli, input_with_timeout, beautiful_exit

if __name__ == "__main__":
    try:
        # Убираем дефолтный логгер
        logger.remove()
        add_logger()
        # Настраиваем компактный формат

        (
            llama_path,
            llama_flags,
            default_llm,
            names_llm,
            dict_llm,
            dict_cmds,
            timeout,
        ) = get_config_data("config.ini", "utf-8")
        psswrd = get_env_data()
        cmd = input_with_timeout(
            prompt="Напишите название LLM для запуска:",
            timeout=timeout,
            names_llm=names_llm,
        )
        strategy = LLMModel(default_llm if (cmd is None) else cmd, dict_llm)
        server_data = ServerData(llama_path, llama_flags)
        runner = LLMServerRunner(strategy, server_data, psswrd)
        runner.start_server()
        cli(runner, names_llm, dict_cmds, dict_llm)
    except ModuleNotFoundError as e:
        print(f"Не смогли загрузить библиотеки: {e}")
        beautiful_exit()
    except KeyboardInterrupt:
        logger.info("Программа завершена вводом: Ctrl + C")
        beautiful_exit()
    except WindowsError:
        logger.critical(f"Не найдена директория: {llama_path}")
        beautiful_exit()
    except Exception as e:
        logger.error(f"Неизвестная ошибка{e}")
        beautiful_exit()
