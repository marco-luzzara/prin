TRAINING_TASK_TYPE='training'
INFERENCE_TASK_TYPE='inference'

def validate_task_type(task_type: str) -> None:
    task_type = task_type.strip()
    if task_type != TRAINING_TASK_TYPE and task_type != INFERENCE_TASK_TYPE:
        raise Exception(f'Task type parameter has an invalid value: "{task_type}"')