import os
import sys
import re

file = open("F:\\Py\\case.txt", "w")
with open("F:\\Py\\FileListsH-all.txt", "r") as fa:
    for line in fa:
        # if not re.search('[(bj)|(Bj)|(BJ)][(ta)|(tb)|o|y|r|-|_]',line):
        #     file.write(line)
        if re.search("(case)|{[0-9],5}", line, re.IGNORECASE):
            file.write(line)


file.close()