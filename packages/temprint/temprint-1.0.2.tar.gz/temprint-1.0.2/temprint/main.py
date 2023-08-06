from .terminalsize import get_terminal_size

__last_temprint_length__ = 0


def temprint(*objs, sep=' '):
    global __last_temprint_length__
    print('\r' + ' '*__last_temprint_length__, end='\r', flush=True)
    msg = sep.join(str(obj) for obj in objs)
    terminal_width, _ = get_terminal_size()
    if len(msg) > terminal_width:
        __last_temprint_length__ = 0
        print(msg, end='\n', flush=True)
    else:
        __last_temprint_length__ = len(msg)
        print(msg, end='', flush=True)
