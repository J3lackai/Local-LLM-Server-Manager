# Local LLM Server Manager

CLI-утилита для управления локальным сервером LLM на базе `llama.cpp`.
Позволяет запускать и переключать модели без изменения кода, используя только конфигурационный файл.

Проект реализует архитектурный паттерн **Strategy** для динамического выбора модели.

---

## Возможности

- 🚀 Запуск `llama-server`
- 🔁 Переключение моделей во время работы
- ⚙️ Добавление новых моделей через `config.ini`
- 📜 Просмотр логов сервера
- 💻 CLI управление
- 🧠 Реализация паттерна Strategy
- 📦 Чистая конфигурационная архитектура

---

## Архитектура

Проект состоит из нескольких компонентов:

| Компонент | Описание |
|-----------|----------|
| `LLMServerRunner` | Контекст: запуск, остановка, перезапуск сервера, вывод логов |
| `LLMModel`        | Стратегия: путь к `.gguf`, параметры запуска, имя модели |
| `config.ini`      | Data-driven стратегии: список моделей и команд |

---

## Установка

### Требования

- Python 3.12.8
- `llama.cpp` (llama-server)
- Модели в формате GGUF

### Клонирование репозитория

```bash
git clone https://github.com/yourname/llm-server-manager
cd llm-server-manager

Установка зависимостей
pip install loguru keyboard
Конфигурация

Все модели задаются в config.ini.

Пример:

[Main]
flags=-m
server_path=C:/llama/llama-server.exe
llm_list = ["qwen", "gpt"]
default_llm = gpt

[commands]
help = Список доступных команд
info = Какая модель запущена
list = Список доступных моделей
exit = Завершить работу

[qwen]
flags=-c 16384 --parallel 1 -ngl 16 -t 12
path=C:/models/qwen.gguf

[gpt]
flags=-c 65536 --parallel 2 -ngl 20
path=C:/models/gpt.gguf
Добавление новой модели

Добавьте секцию в config.ini:

[mistral]
flags=-c 32768 --parallel 2 -ngl 18
path=C:/models/mistral.gguf

Добавьте имя модели в список:

llm_list = ["qwen", "gpt", "mistral"]

После этого модель можно запускать через CLI.

Использование

Запуск программы:

python main.py

Доступна CLI-консоль:

>>> help
>>> list
>>> qwen
>>> gpt
>>> exit
Команды
Команда	Описание
help	список команд
info	текущая модель
list	список моделей
exit	завершение программы
имя модели	запуск модели