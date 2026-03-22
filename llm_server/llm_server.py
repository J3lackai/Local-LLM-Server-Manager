from llm_strategy.llm_strategy import LLMStrategy
import os
import subprocess
from loguru import logger
import threading
from time import sleep
import psutil
from CLI import beautiful_exit


class ServerData:
    def __init__(self, llama_path: str, llama_flags: str, backend: str):
        self.llama_path = llama_path
        self.llama_flags = llama_flags
        self.backend = backend


# ======================
# 4. Контекст: Runner (исполняет стратегию)
# ======================


class LLMServerRunner:
    def __init__(self, strategy: LLMStrategy, server_data: ServerData, psswrd: str):
        self.strategy = strategy
        self.llama_path = server_data.llama_path
        self.llama_flags = server_data.llama_flags
        self.rocm = True if server_data.backend == "rocm" else False
        self.psswrd = psswrd
        self.process = None

    def stop_server(self):
        if self.process:
            # Принудительно убиваем процесс и его дочерние процессы (если есть)
            parent_pid = self.process.pid

            for child in psutil.Process(parent_pid).children(recursive=True):
                logger.info(f"Завершение процесса-ребенка PID {child.pid}...")

        # Убиваем основной процесс принудительно (если terminate не сработал)
        if self.process is not None:
            self.process.kill()  # Более жёсткое завершение, чем terminate()

        if hasattr(self, "process"):
            sleep(1.5)
        self.process = None

        # Пауза для освобождения VRAM на ROCm (важно!)
        sleep(2)

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
        try:
            model_path = self.strategy.get_path()
            flags = self.strategy.get_flags()
            logger.info(model_path)
            if not os.path.exists(model_path):
                raise FileNotFoundError("Модель не найдена")
            command = ""
            for i in (
                self.llama_path,
                self.llama_flags,
                model_path,
                flags,
                "--api-key",
                self.psswrd,
            ):
                command += i + " "
            logger.info(f"Запуск сервера: {self.strategy.get_name()}")
            if self.rocm:
                os.environ["HIP_VISIBLE_DEVICES"] = "0"
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

        except KeyboardInterrupt:
            self.stop_server()
            logger.info("Программа завершена вводом: Ctrl + C")
            beautiful_exit()
        except Exception as e:
            self.stop_server()
            logger.error(f"Ошибка запуска сервера: {e}")
