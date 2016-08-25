"""File to display all found answers to Kevins puzzles"""

from kmpuzzles import puzzles
from kmanswers import answers
from kmlib import *
from base64 import b64decode



if __name__ == '__main__':
    for i,puzzle in enumerate(puzzles):
        answer = answers[i]
        ansval = answer.replace("$input", '"%s"' % puzzle)
        if ansval is "":
            stdout = "UNSOLVED: " + puzzle.replace("\r\n", " ")
        else:
            try:
                stdout = eval(ansval)
            except:
                stdout = "FAILED: " + ansval
            if type(stdout) is bytes:
                stdout = stdout.decode('ascii')
            if " " not in stdout:
                stdout = infer_spaces(stdout)
        print("{:2}".format(i), stdout)
