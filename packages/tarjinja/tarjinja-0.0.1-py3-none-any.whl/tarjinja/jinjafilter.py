from jinja2 import Environment

from .iface import Filter


class JinjaFilter(Filter):
    def __init__(self, **kwargs):
        self.env = Environment(**kwargs)
        self.addfilter("brace", self.brace)

    def addfilter(self, name, fn):
        self.env.filters[name] = fn

    def brace(self, vals):
        if isinstance(vals, (tuple, list)):
            vals = [self.brace(x) for x in vals]
            return "{" + ",".join(vals) + "}"
        return str(vals)

    def render(self, s: str, vals: dict) -> str:
        tmpl = self.env.from_string(s)
        return tmpl.render(**vals)
