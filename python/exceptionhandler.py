import os
import linecache
import sys

def PrintException(e):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    # print('EXCEPTIO({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    print('Traceback (most recent call last):\n  File "{}", line {} in <module>\n    {}\n{}: {}'.format(filename, lineno, line.strip(), type(e).__name__, exc_obj))

def dump_fs(fs, dest_path_fs):
    target_path = dest_path_fs
    os.symlink('node.dat', target_path)
    return 'hallelujah'

def main():
    fs, dest_path_fs = '', ''
    print(dump_fs(fs, dest_path_fs))

import sys, traceback
# import traceback

try:
    main()
    # print(1/0)
except:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    # traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    print(exc_type, exc_value, exc_traceback)

    print("*** print_exception:", file=sys.stdout)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    # print("*** print_exc:")
    # traceback.print_exc(file=sys.stdout)
    print( '-' * 25)
    print("*** format_exc, first and last line:")
    formatted_lines = traceback.format_exc().splitlines()
    print(formatted_lines[0].replace('(most recent call ', '('))
    print(formatted_lines[-3])
    print(formatted_lines[-2])
    print(formatted_lines[-1])
    print('Traceback (complete)')
    print("*** format_exception:")
    print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    print("*** extract_tb:")
    print(repr(traceback.extract_tb(exc_traceback)))
    print("*** format_tb:")
    print(repr(traceback.format_tb(exc_traceback)))
    print("*** tb_lineno:", exc_traceback.tb_lineno)

print('\n' + '-' * 25 + """
Traceback (most recent call last):
  File "C:/Users/wittr/Documents/GitHub/ideone/fiddle.py", line 57, in <module>
    main()
  File "C:/Users/wittr/Documents/GitHub/ideone/fiddle.py", line 53, in main
    print(dump_fs(fs, dest_path_fs))
  File "C:/Users/wittr/Documents/GitHub/ideone/fiddle.py", line 48, in dump_fs
    os.symlink('node.dat', target_path)
OSError: symbolic link privilege not held""")
