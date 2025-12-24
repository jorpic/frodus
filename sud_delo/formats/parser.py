class ParseErr(Exception):
    def __init__(self, message, query):
        super().__init__(f'{message}: {query}')

def x(sel, q, *args):
    if sel == None:
        raise ParseErr('selector is None', q)

    res = sel.xpath(q[2:])
    res_arity = q[0]
    res_kind = q[1]
    single_res = res_arity == '1' or res_arity == '?'

    # Check arity
    valid_arity = (res_arity == '1' and len(res) == 1) \
        or (res_arity == '?' and len(res) <= 1) \
        or (res_arity == '+' and len(res) >= 1) \
        or (res_arity == '*') \
        or (res_arity == '8' and len(res) == 8) \
        or (res_arity == '9' and len(res) == 9)
    if not valid_arity:
        raise ParseErr(f"{len(res)=}", q)

    # Check kind
    if res_kind == 'n':
        pass
    elif res_kind == 't':
        if single_res:
            res = res.get()
        else:
            res = res.getall()
    elif res_kind == 's':
        res = ' '.join([s.strip() for s in res.getall()])
    elif res_kind == 'S':
        res = '\n'.join([s.strip() for s in res.getall()])
    else:
        raise ParseErr('Unexpected kind/arity ', q)

    # Recurse
    if args == ():
        return res
    else:
        if single_res:
            return x(res, *args)
        else:
            return [x(r, *args) for r in res]
