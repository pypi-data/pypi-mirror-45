import time
from typing import Generator, Tuple
from .iface import Input, Output
from logging import getLogger

log = getLogger(__name__)


class MemInput(Input, dict):
    def __init__(self, fn: str):
        super().__init__(fn)
        self.mode = 0o644
        self.ts = time.time()

    def walk(self) -> Generator[Tuple[str, int, float], None, None]:
        for k in self.keys():
            yield k, self.mode, self.ts

    def readfile(self, fn: str) -> str:
        return self.get(fn)


class MemOutput(Output, dict):
    def __init__(self, fn: str):
        super().__init__(fn)

    def writefile(self, fn: str, content: str, mode: int, ts: float = None):
        self[fn] = content
