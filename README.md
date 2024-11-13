# HealthUnity

## Installation and Setup

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set the required API keys by creating `.env` file (see `.env.example`)

## Run Application with Interface

To start the application, run:
```bash
python interface.py
```

## Run Application via Terminal

To start the application, run:
```bash
python main.py
```

## Creating a New Task

To create a new task, follow these steps:

1. Create a new inherited task class in the `./tasks` folder (e.g., `medllm.py` or `pubmed.py`).
2. Assign the task in the following files:
    - `openCHA/tasks/task_types.py`
    - `openCHA/tasks/types.py`

## Testing the Task

To test the functionality of your task, run the following command:
```bash
python test_task.py
```
