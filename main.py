#!/bin/env python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

import time
import os
import toml
import sys


class EllieHandler(FileSystemEventHandler):
    """EllieHandler."""

    def __init__(self, movers):
        """__init__.

        :param movers:
        """
        self.movers = movers

    def on_created(self, event):
        """on_created.

        :param event:
        """
        for move in self.movers:
            if move(event.src_path):
                print("moved")
                return True


def make_mover(folder, rules):
    """make_mover.

    :param folder:
    :param rules:
    """
    print(folder, rules)
    return lambda x: os.rename(x, os.path.join(folder, os.path.basename(x))
                               ) if os.path.splitext(x)[-1] in rules else False


def main(watchpath):
    """main.

    :param watchpath:
    """
    FileExtensions = toml.load(os.path.join(watchpath, "rules.toml"))
    temp = FileExtensions.copy()
    for i in temp:
        path = os.path.join(watchpath, i)
        if not os.path.isdir(path):
            os.mkdir(path)
        FileExtensions[path] = FileExtensions.pop(i)
    movers = [make_mover(i, FileExtensions[i]) for i in FileExtensions]

    observer = Observer()
    observer.schedule(EllieHandler(movers), watchpath)
    observer.start()

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main(sys.argv[1])
