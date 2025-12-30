
class ParseErr(Exception):
    def __init__(self, message, query, res=None):
        super().__init__(f'{message}: {query}, {res}')

def select(sel, *args):
    res = None
    for (path, fn) in args:
        try:
            res = x(sel, *path)
        except:
            pass

        if res:
            if fn:
                return fn(res)
            else:
                return res

    raise ParseErr("no parser selected", args, sel)

def x(sel, q, *args):
    if sel == None:
        raise ParseErr('selector is None', q)

    if type(q) is tuple:
        return tuple((x(sel, qq) for qq in q))

    if callable(q):
        return q(sel) ## FIXME: check args = ()

    res = sel.xpath(q[2:])
    res_arity = q[0]
    res_type = q[1]
    single_res = res_arity in '1?!'

    # Check arity
    if res_arity not in '!?+*0123456789abcdef':
        raise ParseErr('Unknown arity', q)
    valid_arity = False \
        or (res_arity == '!' and len(res) <= 1) \
        or (res_arity == '?' and len(res) <= 1) \
        or (res_arity == '+' and len(res) >= 1) \
        or (res_arity == '*') \
        or (res_arity == f'{len(res):x}') # any hex digit
    if not valid_arity:
        raise ParseErr(f'{len(res)=}', q, sel)

    if len(res) == 0 and res_arity == '?':
        return None

    if res_type == 'n':
        if args == ():
            return res
        if single_res:
            return x(res, *args)
        else:
            return [x(r, *args) for r in res]

    if args != ():
        raise ParseErr('Bug! Recursion is not for prim types', q)

    ## Below we handle only text types, so here is a shortcut.
    if len(res) == 0 and res_arity == '!':
        return ''

    if res_type == 's':
        if single_res:
            return res.get()
        else:
            return res.getall()

    if res_type not in 'tT':
        raise ParseErr('Unexpected {res_type=}', q)

    sep = ' '
    if res_type == 'T':
        sep = '\n'

    if single_res:
        res = res.xpath('.//text()')
        return sep.join([s.strip() for s in res.getall()]).strip()
    else:
        res = (r.xpath('.//text()') for r in res)
        return [
            sep.join([s.strip() for s in r.getall()]).strip()
            for r in res
        ]
