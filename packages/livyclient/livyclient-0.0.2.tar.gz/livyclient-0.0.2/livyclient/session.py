import logging
from typing import Optional, List, Dict, Any

import requests

from models.common import Version
from models.sessions import Session, SessionKind, Statement, StatementKind
from utils.case import underline2hump
from utils.httpclient import JSONResponse

VALID_LEGACY_SESSION_KINDS = {
    SessionKind.SPARK, SessionKind.PYSPARK, SessionKind.PYSPARK3, SessionKind.SPARKR, SessionKind.SQL
}
VALID_SESSION_KINDS = {
    SessionKind.SPARK, SessionKind.PYSPARK, SessionKind.SPARKR, SessionKind.SQL
}
LOGGER = logging.getLogger(__name__)


class LivySession:
    def __init__(self, url: str):
        self._client = JSONResponse(url)
        self._server_version_cache: Optional[Version] = None

    def close(self):
        self._client.close()

    def server_version(self) -> Version:
        if self._server_version_cache is None:
            data = self._client.get('/version')
            self._server_version_cache = Version(data['version'])
        return self._server_version_cache

    def legacy_server(self) -> bool:
        return self.server_version() < Version('0.5.0-incubating')

    def list_sessions(self) -> List[Session]:
        json_response = self._client.get('/sessions')
        return [Session.from_json(item) for item in json_response['sessions']]

    def create_sessions(self, kind: SessionKind, proxy_user: str = None, jars: List[str] = None,
                        py_files: List[str] = None, files: List[str] = None, driver_memory: str = None,
                        driver_cores: int = None, executor_memory: str = None, executor_cores: int = None,
                        num_executors: int = None, archives: List[str] = None, queue: str = None,
                        name: str = None, conf: Dict[str, Any] = None) -> Session:
        keywords = locals()
        keywords.pop('self')

        valid_kinds = VALID_LEGACY_SESSION_KINDS if self.legacy_server() else VALID_SESSION_KINDS
        if kind not in valid_kinds:
            raise ValueError(
                f'{kind} is not a valid session kind for a Livy server of '
                f'this version (should be one of {valid_kinds})'
            )

        keywords.pop('kind')
        body = {underline2hump(k): v for k, v in keywords.items() if v is not None}
        body['kind'] = kind.value
        json_response = self._client.post('/sessions', data=body)
        return Session.from_json(json_response)

    def get_sessions(self, session_id: int) -> Optional[Session]:
        try:
            json_response = self._client.get(f'/sessions/{session_id}')
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                raise
        return Session.from_json(json_response)

    def delete_sessions(self, session_id: int) -> None:
        self._client.delete(f'/sessions/{session_id}')

    def list_statements(self, session_id: int) -> List[Statement]:
        json_response = self._client.get(f'/sessions/{session_id}/statements')
        return [Statement.from_json(session_id, data) for data in json_response['statements']]

    def create_statements(self, session_id: int, code: str, kind: StatementKind = None) -> Statement:
        body = {'code': code}

        if kind is not None:
            if self.legacy_server():
                LOGGER.warning('statement kind ignored on Livy<0.5.0')
            body['kind'] = kind.value
        json_response = self._client.post(f'/sessions/{session_id}/statements', data=body)

        print(body)
        return Statement.from_json(session_id, json_response)

    def get_statements(self, session_id: int, statement_id: int) -> Statement:
        json_response = self._client.get(f'/sessions/{session_id}/statements/{statement_id}')
        return Statement.from_json(session_id, json_response)
