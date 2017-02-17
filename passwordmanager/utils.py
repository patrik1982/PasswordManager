def get_bytes(s):
    if isinstance(s, str):
        s_bytes = s.encode('utf-8')
    elif isinstance(s, bytes):
        s_bytes = s
    elif s is None:
        s_bytes = b""
    else:
        print("Unknown type %s" % (type(s)), s)
        s_bytes = None
    return s_bytes
