config = {}


def get_config(s: str, default: int = 0):
    if s not in config:
        return default
    else:
        return config[s]


def read_config():
    cfg = open(".114514", "r")
    try:
        a = cfg.readline()
        a = a[:-1]
        b = int(cfg.readline())
        config[a] = b
    except:
        pass


def write_config():
    cfg = open(".114514", "w")
    for a in config:
        cfg.write(a + '\n')
        cfg.write(str(config[a]) + '\n')


def change_config(a, b):
    config[a] = b
    write_config()
