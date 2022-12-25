"""This script will add a different folder to sys.path so modules can be loaded from there
i.e. import module from another folder"""
import os
import sys
import inspect


def addfolder(name):
    frame2file = inspect.getfile(inspect.currentframe())
    cmd_sub_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(frame2file)[0], name+'/')))
    if cmd_sub_folder not in sys.path:
        sys.path.insert(0, cmd_sub_folder)
