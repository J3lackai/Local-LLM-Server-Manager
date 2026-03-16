from llm_strategy import LLMStrategy
from loguru import logger


# ======================
# 2. Модель для стратегии
# ======================
class LLMModel(LLMStrategy):
    def __init__(self, name, dict: dict):
        try:
            self.name = name
            self.model_path = dict[name + "_path"]
            self.flags = dict[name + "_flags"]
        except Exception as e:
            self.model_path = ""
            self.flags = ""
            logger.error(f"Проблема с чтением конфига: {e}")

    def get_path(self) -> str:
        return self.model_path

    def get_flags(self) -> list[str]:
        return self.flags

    def get_name(self) -> str:
        list_llm_path = self.model_path.split("\\")
        return list_llm_path[-2] if len(list_llm_path) >= 2 else ""
