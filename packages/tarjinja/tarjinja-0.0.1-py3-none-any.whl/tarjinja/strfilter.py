import string

from .iface import Filter


class TemplateFilter(Filter):
    def render(self, s: str, vals: dict) -> str:
        return string.Template(s).substitute(**vals)


class FormatFilter(Filter):
    def render(self, s: str, vals: dict) -> str:
        return s.format(**vals)


class PercentFilter(Filter):
    def render(self, s: str, vals: dict) -> str:
        return s % vals


class FstringFilter(Filter):
    def render(self, s: str, vals: dict) -> str:
        return eval("f" + repr(s), vals, {})
