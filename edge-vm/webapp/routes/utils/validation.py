TRAINING_SCOPE='training'
INFERENCE_SCOPE='inference'

def validate_scope(scope: str) -> None:
    scope = scope.strip()
    if scope != TRAINING_SCOPE and scope != INFERENCE_SCOPE:
        raise Exception(f'scope parameter has an invalid value: "{scope}"')