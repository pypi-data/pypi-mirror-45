from typing import Optional, List


class LivyClientException(Exception):
    pass


class SparkRuntimeError(LivyClientException):
    def __init__(self, ename: Optional[str], evalue: Optional[str], traceback: Optional[List[str]]) -> None:
        self.ename = ename
        self.evalue = evalue
        self.traceback = traceback

    def __repr__(self):
        name = self.__class__.__name__
        message = []
        if self.ename:
            message.append(f'ename={self.ename!r}')
        if self.evalue:
            message.append(f'evalue={self.evalue!r}')
        return f'{name}({", ".join(message)})'
