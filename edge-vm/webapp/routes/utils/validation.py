import json

TRAINING_SCOPE='training'
INFERENCE_SCOPE='inference'

def validate_scope(scope: str) -> None:
    if scope != TRAINING_SCOPE and scope != INFERENCE_SCOPE:
        raise Exception(f'"scope" parameter has an invalid value: "{scope}"')
    

def validate_entrypoint(entrypoint: str) -> None:
    if entrypoint == '':
        return
    
    try:
        err_msg = '"entrypoint" parameter must be a JSON array of strings with at least 1 element'
        parsed_entrypoint = json.loads(entrypoint)
        
        if not isinstance(parsed_entrypoint, list) or \
            len(parsed_entrypoint) == 0 or \
            any(not isinstance(x, str) for x in parsed_entrypoint):
            raise Exception(err_msg)
    except json.decoder.JSONDecodeError:
        raise Exception(f'"entrypoint" parameter is not a valid json')
    