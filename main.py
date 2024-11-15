import os, sys

sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv

load_dotenv()

from openCHA import openCHA
from prompts import MAIN_PROMPT

available_tasks = [
    "medline_search",
    "pubmed_search",
    "medical_llm",
    "merlin_task",
    "google_translate",
    "deid_task",
]


kwargs = {"model_name": "gpt-4o", "response_generator_prefix_prompt": MAIN_PROMPT}

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
