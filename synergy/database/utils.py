from collections import namedtuple

def listify(payload):
    SQLInsert = namedtuple('SQLInsert', 'keys vals placeholders columns')
    keys = list(payload.keys())
    vals = list(payload.values())
    placeholders = ', '.join(['%s'] * len(vals))
    columns = ', '.join(keys)
    return SQLInsert(keys, vals, placeholders, columns)
