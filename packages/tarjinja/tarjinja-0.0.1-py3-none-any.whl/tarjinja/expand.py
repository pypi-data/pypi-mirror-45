import ast
import re
import itertools
from typing import Generator


def list_expand(s: str) -> Generator[str, None, None]:
    """
    >>> list(list_expand("abc [1,2,3] def ['abc', 'def'] xyz"))
    ['abc 1 def abc xyz', 'abc 1 def def xyz', 'abc 2 def abc xyz', 'abc 2 def def xyz', 'abc 3 def abc xyz', 'abc 3 def def xyz']
    """
    args = []
    cur = 0
    for i in re.finditer("\\[[^\\[\\]]*\\]", s):
        st, en = i.span()
        val = ast.literal_eval(s[st:en])
        if cur < st:
            args.append([s[cur:st]])
        args.append(val)
        cur = en
    if cur < len(s):
        args.append([s[cur:]])

    for v in itertools.product(*args):
        yield "".join(map(str, v))
