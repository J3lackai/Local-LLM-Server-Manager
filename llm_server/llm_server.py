from llm_strategy.llm_strategy import LLMStrategy
import os
import subprocess
from loguru import logger
import threading


class ServerData:
    def __init__(self, llama_path: str, llama_flags: str):
        self.llama_path = llama_path
        self.llama_flags = llama_flags


# ======================
# 4. Контекст: Runner (исполняет стратегию)
# ======================


class LLMServerRunner:
    def __init__(self, strategy: LLMStrategy, server_data: ServerData, psswrd: str):
        self.strategy = strategy
        self.llama_path = server_data.llama_path
        self.llama_flags = server_data.llama_flags
        self.psswrd = psswrd
        self.process = None

    def stop_server(self):

        if self.process and self.process.poll() is None:
            logger.info("⛔ Остановка сервера...")
            self.process.terminate()
            self.process.wait()
        logger.success("Работа сервера завершена! ✅")

    def restart_server(self):

        self.stop_server()
        self.start_server()

    def set_strategy(self, strategy):
        self.strategy = strategy
        logger.info(f"Стратегия изменена на: {strategy.get_name()}")

    def _log_reader(self):
        """Читает stdout сервера и выводит логи."""
        for line in self.process.stdout:
            logger.info(line.strip())

    def start_server(self):

        model_path = self.strategy.get_path()
        flags = self.strategy.get_flags()
        logger.info(model_path)
        if not os.path.exists(model_path):
            raise FileNotFoundError("Модель не найдена")

        if not os.path.exists(self.llama_path):
            raise FileNotFoundError("llama-server.exe не найден")
        command = ""
        api = f"--api-key {self.psswrd}"
        for i in (self.llama_path, self.llama_flags, model_path, flags, api):
            command += i + " "
        logger.info(command)
        logger.info(f"🚀 Запуск сервера: {self.strategy.get_name()}")

        try:
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                shell=False,
            )

            # поток для логов
            log_thread = threading.Thread(target=self._log_reader, daemon=True)

            log_thread.start()
            logger.info("Скоро сервер запустится...")
        except Exception as e:
            logger.error(f"Ошибка запуска сервера: {e}")
