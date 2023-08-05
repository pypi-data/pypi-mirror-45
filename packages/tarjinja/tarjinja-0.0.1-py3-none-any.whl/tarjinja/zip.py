import datetime
import time
import zipfile
from typing import Generator, Tuple
from logging import getLogger
from .iface import Input, Output

log = getLogger(__name__)


class ZipInput(Input):
    def __init__(self, ifn: str):
        super().__init__(ifn)
        self.zf = zipfile.ZipFile(ifn)
        self.encoding = "utf-8"
        self.ZIP_UNIX_SYSTEM = 3

    def walk(self) -> Generator[Tuple[str, int, float], None, None]:
        for zinfo in self.zf.infolist():
            if zinfo.is_dir():
                continue
            ts = datetime.datetime(*zinfo.date_time)
            mode = 0o644
            if zinfo.create_system == self.ZIP_UNIX_SYSTEM:
                mode = zinfo.external_attr >> 16
            yield zinfo.filename, mode, ts.timestamp()

    def readfile(self, fn: str) -> str:
        return self.zf.read(fn).decode(self.encoding)


class ZipOutput(Output):
    def __init__(self, ofn: str):
        super().__init__(ofn)
        self.zf = zipfile.ZipFile(ofn, "w")
        self.encoding = "utf-8"
        self.compress_type = zipfile.ZIP_DEFLATED

    def writefile(self, fn: str, content: str, mode: int, ts: float = None):
        zinfo = zipfile.ZipInfo(fn, time.localtime(ts))
        zinfo.compress_type = self.compress_type
        zinfo.external_attr = mode << 16
        if ts is not None:
            tm = time.localtime(ts)
            zinfo.date_time = (tm.tm_year, tm.tm_mon, tm.tm_mday,
                               tm.tm_hour, tm.tm_min, tm.tm_sec)
        self.zf.writestr(zinfo, content)

    def finish(self):
        self.zf.close()
