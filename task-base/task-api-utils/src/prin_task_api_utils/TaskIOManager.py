import io
from typing import Generator, Tuple, Dict
import tempfile
from contextlib import contextmanager

import requests


ResultFile = Tuple[str, io.BytesIO]

class TaskIOManager:
    def __init__(self, task_api_base_url: str):
        self.__task_api_base_url = task_api_base_url

    
    def save_model(self, model_file: io.BytesIO, user_group: str) -> requests.Response:
        """Send a POST request to '{task_api_base_url}/models' to persistently save the model

        :param model_file: file-like object representing the model. Make sure the file pointer
            is located at the beginning of the file to save the entire model, otherwise use `seek(0)`.
        :type model_file: io.BytesIO
        :param user_group: the group of the user that has initiated the task
        :type user_group: str
        :returns: The response sent by the Task API server
        :rtype: requests.Response
        """

        files = {'model_file': ('model.sav', model_file)}
        save_model_req_params = { 'group_name': user_group }
        save_model_response = requests.post(f'{self.__task_api_base_url}/models', 
                                            params=save_model_req_params, 
                                            files=files)
        
        return save_model_response
    

    @contextmanager
    def get_model(self, 
                  user_group: str, 
                  model_version: str = 'latest', 
                  chunk_size: int = 16384) -> Generator[io.BytesIO, None, None]:
        """Send a GET request to '{task_api_base_url}/models' to get the model with the specified
        version.

        :param user_group: the group of the user that has initiated the task
        :type user_group: str
        :param model_version: version of the model to retrieve (default: 'latest')
        :type model_version: str
        :param chunk_size: the API response returns a stream object and `chunk_size` is 
            the number of bytes it should read into memory (default: 16384)
        :type chunk_size: int
        :returns: The model file
        :rtype: io.BytesIO
        """

        try:
            model_file = tempfile.TemporaryFile()

            get_model_req_params = { 'group_name': user_group }
            with requests.get(f'{self.__task_api_base_url}/models/{model_version}', 
                            params=get_model_req_params, 
                            stream=True) as get_model_response:
                for chunk in get_model_response.iter_content(chunk_size=chunk_size):
                    model_file.write(chunk)

            model_file.seek(0)
            yield model_file
        finally:
            model_file.close()


    def save_results(self, 
                     results: Dict[str, ResultFile], 
                     user_group: str, 
                     task_scope: str) -> requests.Response:
        """Send a POST request to '{task_api_base_url}/results/{task_scope}' to persistently save the
            task results

        :param results: dictionary of file description. The key is the file id; the value is a tuple
            where the first element is the filename, the second one is a file-like object representing
            the task result. Make sure the file pointer is located at the beginning of the file 
            to save the entire model, otherwise use `seek(0)`. 
        :type results: Dict[str, ResultFile]
        :param user_group: the group of the user that has initiated the task
        :type user_group: str
        :param task_scope: the task scope (inference|training)
        :type task_scope: str
        :returns: The response sent by the Task API server
        :rtype: requests.Response
        """

        save_result_req_params = { 'group_name': user_group }
        save_result_response = requests.post(f'{self.__task_api_base_url}/results/{task_scope}', 
                                             params=save_result_req_params, 
                                             files=results)
        
        return save_result_response
