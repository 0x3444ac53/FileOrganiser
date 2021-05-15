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
import watch_object
from multiprocessing import Pool
import re


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
    mode = rules.pop("mode").lower()
    for i in rules:
        path = os.path.join(os.path.split(filePath)[0], i)
        if not os.path.isdir(path):
            os.mkdir(path)
        rules[path] = rules.pop(i)
    ruleHandler = importlib.import_module(f"modes.{mode}")
    print(rules)
    return [ruleHandler.make_mover(i, rules[i]) for i in rules]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('watchpath', help='The Directory to watch')
    p.add_argument('-d', '--daemon', help="run as daemon", action='store_true')
    p.add_argument('-r',
                   '--recursive',
                   help="Crawl down directories",
                   action='store_true')
    return p.parse_args()


def recursiveHandler(path, pattern):
    watchpaths = []
    for root, dirs, files in os.walk(path):
        if any(pattern.match(file) for file in files):
            watchpaths.append(root)
    return watchpaths


def clean(rootwatchpath, daemon, recursive=False):
    watchpaths = []
    watchedDirs = []
    watchpaths.append(rootwatchpath)
    pat = re.compile("rules\d*.toml")
    if recursive:
        watchpaths = recursiveHandler(rootwatchpath, pat)
    print(watchpaths)
    for watchpath in watchpaths:
        # Flattens the list
        rules = [
            i for x in [
                loadconfig(os.path.join(watchpath, i)) for i in filter(
                    lambda x: x[-4:] == "toml",
                    filter(lambda x: x[:5] == "rules", os.listdir(watchpath)))
            ] for i in x
        ]
        print(rules)
        handler = EllieHandler(rules)
        handler.clean(watchpath)
        if daemon:
            watchedDirs.append(Observer())
            watchedDirs[-1].schedule(handler, watchpath)
            watchedDirs[-1].start()
            try:
                while True:
                    time.sleep(100)
            except KeyboardInterrupt:
                for observer in watchedDirs:
                    observer.stop()
                    observer.join()


if __name__ == "__main__":
    args = parse_args()
    clean(args.watchpath, args.daemon, recursive=args.recursive)
