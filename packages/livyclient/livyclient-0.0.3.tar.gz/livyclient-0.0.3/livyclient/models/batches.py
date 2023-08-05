from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, List, Any, Optional


@unique
class BatchState(Enum):
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


@dataclass()
class State:
    batch_id: int
    state: BatchState

    @classmethod
    def from_json(cls, data: Dict) -> 'State':
        return cls(
            data['id'],
            BatchState(data['state'])
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            'batch_id': self.batch_id,
            'state': self.state.value
        }


@dataclass()
class Log:
    batch_id: int
    log: List[str]

    @classmethod
    def from_json(cls, data: Dict) -> 'Log':
        return cls(
            data['id'],
            data['log']
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            'batch_id': self.batch_id,
            'log': self.log
        }


@dataclass()
class Batch:
    batch_id: int
    name: str
    appId: Optional[str]
    state: BatchState

    @classmethod
    def from_json(cls, data: Dict) -> 'Batch':
        return cls(
            data['id'],
            data['name'],
            data['appId'],
            BatchState(data['state'])
        )

    def as_dict(self) -> Dict[str, Any]:
        return {
            'batch_id': self.batch_id,
            'name': self.name,
            'appId': self.appId,
            'state': self.state.value
        }
