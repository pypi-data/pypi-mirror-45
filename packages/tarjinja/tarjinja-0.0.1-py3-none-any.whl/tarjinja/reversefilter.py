from logging import getLogger
from .iface import Filter

log = getLogger(__name__)


class AbstractReverseFilter(Filter):
    def placeholder(self, name: str) -> str:
        raise NotImplementedError("placeholder")

    def render(self, s: str, vals: dict) -> str:
        res = s
        for k, v in vals.items():
            if isinstance(v, (tuple, list, dict)):
                continue
            res = res.replace(str(v), self.placeholder(k))
        if res != s:
            log.debug("changed: %s <- %s", repr(res[:100]), repr(s[:100]))
        return res


class ReverseJinjaFilter(AbstractReverseFilter):
    def placeholder(self, name: str) -> str:
        return "{{" + name + "}}"


class ReverseTemplateFilter(AbstractReverseFilter):
    def placeholder(self, name: str) -> str:
        return "${" + name + "}"


class ReverseFormatFilter(AbstractReverseFilter):
    def placeholder(self, name: str) -> str:
        return "{" + name + "}"


class ReversePercentFilter(AbstractReverseFilter):
    def placeholder(self, name: str) -> str:
        return "%(" + name + ")s"


class ReverseFstringFilter(ReverseFormatFilter):
    pass
