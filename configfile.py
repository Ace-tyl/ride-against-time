config = {}


def get_config(s: str):
    if s not in config:
        return 0
    else:
        return config[s]


def read_config():
    cfg = open(".114514", "r")
    try:
        a = cfg.readline()
        b = int(cfg.readline())
        config[a] = b
    except:
        pass
