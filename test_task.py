import os, sys
sys.path.insert(0, os.getcwd())

from openCHA.tasks.initialize_task import initialize_task

tasks = ["pubmed_search", "medical_llm"]
for task_name in tasks:
    print(task_name)
    task = initialize_task(task_name)
    print(task._execute(["Viral Enteritis in CT"]))
    print("*"*5)