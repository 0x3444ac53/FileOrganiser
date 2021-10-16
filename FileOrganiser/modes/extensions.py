import os

def make_mover(folder, rules):
    return lambda x: os.rename(x, os.path.join(folder, os.path.basename(x))
                               ) if os.path.splitext(x)[-1] in rules else False
