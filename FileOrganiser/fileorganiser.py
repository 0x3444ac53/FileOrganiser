#!/bin/env python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

import os
import toml
import importlib
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

    def on_modified(self, event):
        print(event)

    def clean(self, directory):
        for i in os.listdir(directory):
            pathToFile = os.path.join(directory, i)
            for move in self.movers:
                if move(pathToFile):
                    break

class FileOrganiser:
    def __init__(self, rootwatchpath, recursive=False):
        self.rootwatchpath = rootwatchpath
        self.recursive = recursive
        self.watchedDirs = []
        watchpaths = []
        watchpaths.append(rootwatchpath)
        self.handlers = dict()
        pat = re.compile("rules\d*.toml")
        if recursive:
            watchpaths = self.recursiveHandler(rootwatchpath, pat)
        print(watchpaths)
        for watchpath in watchpaths:
            print("watchpath = {}".format(watchpath))
            rules = [self.loadconfig(os.path.join(watchpath, i)) for i in
                    os.listdir(watchpath) if pat.match(i)][::-1]
            # flatten the list 
            rules = [item for sublist in rules for item in sublist]
            print(rules)
            self.handlers[watchpath] = EllieHandler(rules)
            self.watchedDirs.append(Observer())
            self.watchedDirs[-1].schedule(self.handlers[watchpath], watchpath)
    
    def clean(self):
        for directory in self.handlers.keys():
            self.handlers[directory].clean(directory)

    def start(self):
        for observer in self.watchedDirs:
            observer.start()

    def stop(self):
        for observer in self.watchedDirs:
            observer.stop()
            observer.join()

    def loadconfig(self, filePath):
        rules = toml.load(filePath)
        absolute_path_rules = dict()
        try:
            mode = rules.pop("mode").lower()
        except KeyError:
            print(f"No mode specified {filePath}")
            exit(1)
        for rule in rules:
            path = os.path.join(os.path.split(filePath)[0], rule)
            if not os.path.isdir(path):
                os.mkdir(path)
            absolute_path_rules[path] = rules[rule]
        ruleHandler = importlib.import_module(f"FileOrganiser.modes.{mode}")
        return [ruleHandler.make_mover(i, absolute_path_rules[i]) for i in
                absolute_path_rules]

    def recursiveHandler(self, path, pattern):
        watchpaths = []
        for root, dirs, files in os.walk(path):
            if any(pattern.match(file) for file in files):
                watchpaths.append(root)
        return watchpaths

    
