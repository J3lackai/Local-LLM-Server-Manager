from llm_strategy import LLMStrategy
from loguru import logger


# ======================
# 3. стратегия: GPT-OSS-20B
# ======================
class GPT_20B(LLMStrategy):
    def __init__(self, dict: dict):
        try:
            self.model_path = dict["gpt_path"]
            self.flags = dict["gpt_flags"]
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
