def run_task():
    import os
    import json
    import tempfile
    from prin_task_api_utils import TaskIOManager

    from sqlalchemy import create_engine
    import pandas as pd
    import requests

    TRINO_USER = os.getenv('TRINO_USER')
    TRINO_GROUP = os.getenv('TRINO_GROUP')
    TRINO_ENDPOINT = os.getenv('TRINO_ENDPOINT')
    TRINO_CATALOG = os.getenv('TRINO_CATALOG')
    TRINO_SCHEMA = os.getenv('TRINO_SCHEMA')
    TASK_SCOPE = os.getenv('TASK_SCOPE')
    TASK_APIS_BASE_URL = os.getenv('TASK_APIS_BASE_URL')

    taskIOManager = TaskIOManager(task_api_base_url=TASK_APIS_BASE_URL)


    engine = create_engine(f'trino://{TRINO_USER}@{TRINO_ENDPOINT}/{TRINO_CATALOG}/{TRINO_SCHEMA}')
    connection = engine.connect()

    print('--------------- Testing Trino read ---------------')
    df = pd.read_sql('SELECT * FROM patients', connection)
    print(f"Rows, Columns = {df.shape}")


    print('--------------- Testing model saving ---------------')
    MODEL_FILE_CONTENT = 'prin model'
    print(f'Saving model with content "{MODEL_FILE_CONTENT}"...')
    with tempfile.TemporaryFile() as model_file:
        model_file.write(MODEL_FILE_CONTENT.encode())
        model_file.seek(0)

        save_model_response = taskIOManager.save_model(model_file=model_file, user_group=TRINO_GROUP)


    print(f'Model saved, response: {json.dumps(save_model_response.json())}')


    print('--------------- Testing model get ---------------')
    print('Getting model...')
    with taskIOManager.get_model(user_group=TRINO_GROUP) as model_file:
        print(f'Model retrieved with content "{model_file.read().decode()}"')


    print('--------------- Testing results saving ---------------')
    RESULT_FILE_CONTENT = "task result"
    RESULT_FILE_ID = "result_file"
    print(f'Saving result with content "{RESULT_FILE_CONTENT}"...')
    with tempfile.TemporaryFile() as result_file:
        result_file.write(RESULT_FILE_CONTENT.encode())
        result_file.seek(0)

        save_result_response = taskIOManager.save_results(results={
                RESULT_FILE_ID: ("result.txt", result_file)
            },
            user_group=TRINO_GROUP,
            task_scope=TASK_SCOPE)
        
        pre_signed_url = save_result_response.json()[RESULT_FILE_ID]


    print('--------------- Testing Pre-signed URL ---------------')
    with requests.get(pre_signed_url, stream=True) as get_result_response, tempfile.TemporaryFile() as result_file:
        for chunk in get_result_response.iter_content(chunk_size=16384):
            result_file.write(chunk)

        result_file.seek(0)
        print(f'Result retrieved with content "{result_file.read().decode()}"')


if __name__ == '__main__':
    run_task()
