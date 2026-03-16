from qwen_30b import Qwen_30B
from gpt_20b import GPT_20B
from load_data import get_config_data, get_env_data
from llm_server import LLMServerRunner, ServerData

if __name__ == "__main__":
    llama_path, llama_flags, dict_llm = get_config_data("config.ini", "utf-8")
    psswrd = get_env_data()

    strategy = Qwen_30B(dict_llm)
    server_data = ServerData(llama_path, llama_flags)

    runner = LLMServerRunner(strategy, server_data, psswrd)

    runner.start_server()

    while True:
        cmd = input(">>> ").strip().lower()

        if cmd == "qwen":
            runner.set_strategy(Qwen_30B(dict_llm))
            runner.restart_server()

        elif cmd == "gpt":
            runner.set_strategy(GPT_20B(dict_llm))
            runner.restart_server()

        elif cmd == "exit":
            runner.stop_server()
            break
