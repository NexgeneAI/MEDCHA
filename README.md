# HealthUnity

## Installation and Setup

1. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set the required API keys: (for Windows use `set`, else you can use `export`)
    ```bash
    set OPENAI_API_KEY=your_openai_api_key
    set nvidia_api_key=your_nvidia_api_key
    ```

## Running the Application

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
