#!/bin/env python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

import time
import os
import toml
import sys
import re
import importlib


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

    def clean(self, directory):
        for i in os.listdir(directory):
            pathToFile = os.path.join(directory, i)
            for move in self.movers:
                if move(pathToFile):
                    break


def loadconfig(filePath):
    rules = toml.load(filePath)
    a = rules.pop("mode").lower()
    temp = rules.copy()
    for i in temp:
        path = os.path.join(os.path.split(filePath)[0], i)
        print(path)
        if not os.path.isdir(path):
            os.mkdir(path)
        rules[path] = rules.pop(i)
    ruleHandler = importlib.import_module(f"modes.{a}")
    print(rules)
    return [ruleHandler.make_mover(i, rules[i]) for i in rules]


def main(watchpath):
    """main.

    :param watchpath:
    """
    rules = loadconfig(os.path.join(watchpath,"rules.toml"))
    handler = EllieHandler(rules)
    handler.clean(watchpath)
    observer = Observer()
    observer.schedule(handler, watchpath)
    observer.start()

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main(sys.argv[1])
