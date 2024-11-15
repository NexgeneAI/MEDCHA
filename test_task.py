import os, sys

sys.path.insert(0, os.getcwd())

from dotenv import load_dotenv

load_dotenv()

from openCHA.tasks.initialize_task import initialize_task

task_name = "medical_llm"
print(task_name)
task = initialize_task(task_name)
print(task._execute(["what is Viral Enteritis in CT"]))
print("*" * 5)

task_name = "merlin_task"
print(task_name)
task = initialize_task(task_name)
print(task._execute(["data/image1.nii.gz"]))
print("*" * 5)


task_name = "deid_task"
print(task_name)
task = initialize_task(task_name)
print(
    task._execute(
        [
            "Patient John Doe was admitted to New York Hospital on 10th October 2023 under Dr. Smith's care."
        ]
    )
)
print("*" * 5)

task_name = "medline_search"
print(task_name)
task = initialize_task(task_name)
print(task._execute(["diabetes"]))
print("*" * 5)

task_name = "pubmed_search"
print(task_name)
task = initialize_task(task_name)
print(task._execute(["diabetes"]))
print("*" * 5)
