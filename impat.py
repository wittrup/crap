"""This script will add a different folder to sys.path so modules can be loaded from there
i.e. import module from another folder"""
import os, sys, inspect


def addfolder(name):
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0],name+'/')))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
