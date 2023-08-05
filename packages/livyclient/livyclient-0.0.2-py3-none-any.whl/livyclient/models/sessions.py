from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional, Dict, List, Any

from exceptions import SparkRuntimeError


@unique
class StatementKind(Enum):
    SPARK = 'spark'
    PYSPARK = 'pyspark'
    SPARKR = 'sparkr'
    SQL = 'sql'


@unique
class StatementState(Enum):
    WAITING = 'waiting'
    RUNNING = 'running'
    AVAILABLE = 'available'
    ERROR = 'error'
    CANCELLING = 'cancelling'
    CANCELLED = 'cancelled'


@unique
class OutputStatus(Enum):
    OK = 'ok'
    ERROR = 'error'


@dataclass(frozen=True)
class Output:
    status: OutputStatus
    execution_count: int
    text: Optional[str]
    json: Optional[Dict[str, Any]]
    ename: Optional[str]
    evalue: Optional[str]
    traceback: Optional[List[str]]

    @classmethod
    def from_json(cls, data: Dict) -> 'Output':
        return cls(
            OutputStatus(data['status']),
            data.get('execution_count'),
            data.get('data', {}).get('text/plain'),
            data.get('data', {}).get('application/json'),
            data.get('ename'),
            data.get('evalue'),
            data.get('traceback')
        )

    def as_dict(self) -> Dict:
        return {
            'status': self.status.value,
            'execution_count': self.execution_count,
            'text': self.text,
            'json': self.json,
            'ename': self.ename,
            'evalue': self.evalue,
            'traceback': self.traceback
        }

    def raise_for_status(self) -> None:
        if self.status == OutputStatus.ERROR:
            raise SparkRuntimeError(self.ename, self.evalue, self.traceback)


@dataclass(frozen=True)
class Statement:
    session_id: int
    statement_id: int
    code: str
    state: StatementState
    output: Optional[Output]

    @classmethod
    def from_json(cls, session_id: int, data: Dict) -> 'Statement':
        output = Output.from_json(data['output']) if data['output'] is not None else None
        return cls(
            session_id,
            data['id'],
            data['code'],
            StatementState(data['state']),
            output
        )

    def as_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'statement_id': self.statement_id,
            'code': self.code,
            'state': self.state.value,
            'output': self.output.as_dict() if self.output else None
        }


@unique
class SessionKind(Enum):
    SPARK = 'spark'
    PYSPARK = 'pyspark'
    SPARKR = 'sparkr'
    SQL = 'sql'
    PYSPARK3 = 'pyspark3'


@unique
class SessionState(Enum):
    NOT_STARTED = 'not_started'
    STARTING = 'starting'
    RECOVERING = 'recovering'
    IDLE = 'idle'
    RUNNING = 'running'
    BUSY = 'busy'
    SHUTTING_DOWN = 'shutting_down'
    ERROR = 'error'
    DEAD = 'dead'
    KILLED = 'killed'
    SUCCESS = 'success'


@dataclass(frozen=True)
class Session:
    session_id: int
    name: str
    appId: Optional[str]
    kind: SessionKind
    state: SessionState

    @classmethod
    def from_json(cls, data: Dict) -> 'Session':
        return cls(
            data['id'],
            data['name'],
            data['appId'],
            SessionKind(data['kind']),
            SessionState(data['state']),
        )

    def as_dict(self) -> Dict:
        return {
            'session_id': self.session_id,
            'name': self.name,
            'appId': self.appId,
            'kind': self.kind.value,
            'state': self.state.value
        }
