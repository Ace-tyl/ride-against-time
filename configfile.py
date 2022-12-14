config = {}


def get_config(s: str, default: int = 0):
    if s not in config:
        return default
    else:
        return config[s]


def read_config():
    try:
        cfg = open(".114514", "r").read().split('\n')
        for i in range(0, len(cfg), 2):
            a = cfg[i]
            try:
                b = int(cfg[i + 1])
            except:
                b = float(cfg[i + 1])
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
