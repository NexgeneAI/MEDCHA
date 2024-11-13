import os, sys

sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv

load_dotenv()

from openCHA.tasks.initialize_task import initialize_task

tasks = ["pubmed_search", "medical_llm"]
for task_name in tasks:
    print(task_name)
    task = initialize_task(task_name)
    print(task._execute(["Viral Enteritis in CT"]))
    print("*" * 5)

task_name = "merlin_task"
print(task_name)
task = initialize_task("merlin_task")
print(task._execute(["data/image1.nii.gz"]))
print("*" * 5)
