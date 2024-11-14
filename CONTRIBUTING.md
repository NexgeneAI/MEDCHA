# Contributing to HealthUnity

Thank you for your interest in contributing! Follow these steps to create, test, and submit your contributions.

## Setting Up

1. **Fork and Clone**: Fork this repository and clone it locally.
2. **Install Dependencies**: Run:
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up Environment Variables**: Copy `.env.example` to `.env` and add your API keys.

## Creating a New Task

1. **Define the Task Class**: Create a new inherited task class in the `./tasks` folder, such as `medllm.py` or `pubmed.py`.
2. **Register the Task**:
    - Add the task in `openCHA/tasks/task_types.py`
    - Update `openCHA/tasks/types.py` to include it.

## Testing Your Task

To test your task, run:

```bash
python test_task.py
