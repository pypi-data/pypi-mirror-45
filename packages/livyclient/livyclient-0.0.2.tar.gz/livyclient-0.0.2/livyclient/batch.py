from typing import List, Dict, Any

from models.batches import Batch, State, Log
from utils.case import underline2hump
from utils.httpclient import JSONResponse


class LivyBatch:
    def __init__(self, url: str):
        self._client = JSONResponse(url)

    def close(self):
        self._client.close()

    def list_batches(self) -> List[Batch]:
        json_response = self._client.get('/batches')
        return [Batch.from_json(item) for item in json_response['sessions']]

    def create_batches(self, file: str, proxy_user: str = None, class_name: str = None,
                       args: List[str] = None, jars: List[str] = None, py_files: List[str] = None,
                       files: List[str] = None, driver_memory: str = None, driver_cores: int = None,
                       executor_memory: str = None, executor_cores: int = None, num_executors: int = None,
                       archives: List[str] = None, queue: str = None, name: str = None, conf: Dict[str, Any] = None
                       ) -> Batch:
        """
        Create batch session.
        :param file: File containing the application to execute.
        :param proxy_user: User to impersonate when running the job.
        :param class_name: Application Java/Spark main class.
        :param args: Command line arguments for the application.
        :param jars: jars to be used in this session.
        :param py_files: Python files to be used in this session.
        :param files: files to be used in this session.
        :param driver_memory: Amount of memory to use for the driver process.
        :param driver_cores: Number of cores to use for the driver process.
        :param executor_memory: Amount of memory to use per executor process.
        :param executor_cores: Number of cores to use for each executor.
        :param num_executors: Number of executors to launch for this session.
        :param archives: Archives to be used in this session.
        :param queue: The name of the YARN queue to which submitted.
        :param name: The name of this session.
        :param conf: Spark configuration properties.
        :return: Batch object.
        """
        keywords = locals()
        keywords.pop('self')
        body = {underline2hump(k): v for k, v in keywords.items() if v is not None}
        for k, v in keywords.items():
            if v is not None:
                body[underline2hump(k)] = v

        json_response = self._client.post('/batches', data=body)
        return Batch.from_json(json_response)

    def get_batches(self, batch_id: int) -> Batch:
        json_response = self._client.get(f'/batches/{batch_id}')
        return Batch.from_json(json_response)

    def delete_batches(self, batch_id: int) -> None:
        self._client.delete(f'/batches/{batch_id}')

    def get_state(self, batch_id: int) -> State:
        json_response = self._client.get(f'/batches/{batch_id}')
        return State.from_json(json_response)

    def get_log(self, batch_id: int) -> Log:
        json_response = self._client.get(f'/batches/{batch_id}')
        return Log.from_json(json_response)
