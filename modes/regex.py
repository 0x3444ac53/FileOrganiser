import re
import os 

def make_mover(folder, pattern):
    pattern = re.compile(pattern)
    def tester(x):
        if pattern.search(os.path.basename(x)) and not os.path.isdir(x):
            os.rename(x, os.path.join(folder, os.path.basename(x)))
        else:
            return False
        return True
    return tester

