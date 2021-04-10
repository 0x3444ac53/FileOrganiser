import importlib.util
def make_mover(folder, script):
    spec = importlib.util.spec_from_file_location("aScript", script)
    aScript = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aScript)
    return aScript.main
