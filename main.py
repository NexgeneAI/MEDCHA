import os, sys
sys.path.insert(0, os.getcwd())

from openCHA import openCHA
from prompts import MAIN_PROMPT
available_tasks = ["pubmed_search", "medical_llm"]


kwargs = {
    "model_name": "gpt-4o",
    "response_generator_prefix_prompt": MAIN_PROMPT
}

chat_history = []
while True:
    user_query = input("Ask your question: ")
    cha = openCHA()
    response = cha.run(
        user_query,
        chat_history=chat_history,
        available_tasks=available_tasks,
        use_history=True,
        **kwargs
    )
    print("CHA: ", response)

    chat_history.append((user_query, response))