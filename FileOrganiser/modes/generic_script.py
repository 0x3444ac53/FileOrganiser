import subprocess

def make_mover(folder, script):
    def mover(filename):
        subprocess.Popen([script, filename])
    return mover
