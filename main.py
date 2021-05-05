#!/bin/env python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

import time
import os
import toml
import sys
import re
import importlib
import argparse


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

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('watchpath',
                   help='The Directory to watch')
    p.add_argument('-r', "--rulefile",
                   help="specify config path")
    p.add_argument('-d', '--daemon', help="run as daemon",
                   action='store_true')
    return p.parse_args()

def main():
    """main
    """
    args = parse_args()
    print(args)
    watchpath = args.watchpath
    rules = [i for x in [loadconfig(os.path.join(args.watchpath, i)) for i in
                    filter(lambda x : x[-4:] == "toml",
                       filter(lambda x: x[:5] == "rules",
                              os.listdir(args.watchpath)))] for i in
             x]
    print(rules)
    handler = EllieHandler(rules)
    handler.clean(watchpath)
    if args.daemon:
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
    main()
