from abc import ABC, abstractmethod


# ======================
# 1. Абстрактная Стратегия (интерфейс)
# ======================
class LLMStrategy(ABC):
    @abstractmethod
    def get_path(self) -> str:
        pass

    @abstractmethod
    def get_flags(self) -> list[str]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
