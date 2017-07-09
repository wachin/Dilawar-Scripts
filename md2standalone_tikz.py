#!/usr/bin/env python

"""md2html.py: Convert pandoc markdown to html to be used with jekyll.

Last modified: Sat Jan 18, 2014  05:01PM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, NCBS Bangalore"
__credits__          = ["NCBS Bangalore", "Bhalla Lab"]
__license__          = "GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@iitb.ac.in"
__status__           = "Development"

import sys
import os
import re
import subprocess
import shlex
import time

def waitTillWritten(filename):
    max_i = 10
    for i in xrange(max_i):
        try:
            with open(filename, 'rb') as _:
                break
        except IOError:
            time.sleep(3)
    else:
        raise IOError('Could not access {} after {} attempts'.format(
            filename
            , str(max_i))
            )

def extractFigures(txt):
    global figs
    imagePat = re.compile(
            r'\\usetikzlibrary.+?\\begin\{tikzpicture\}.+?\\end\{tikzpicture\}'
            , re.IGNORECASE | re.DOTALL
            )
    tikzs = imagePat.findall(txt)
    for i, t in enumerate(tikzs):
        txt = txt.replace(t, "\includegraphics[]{image%s.pdf}" % i)
        convertToImage(t, "image{}.tex".format(i))
    return txt


def convertToImage(imageText, filename):
    header = []
    header.append("\\documentclass[tikz]{standalone}")
    header.append("\\begin{document}")
    header.append("")
    footer = [""]
    footer.append("\\end{document}")
    txt = "\n".join(header) + imageText + "\n".join(footer)
    with open(filename, "w") as f:
        f.write(txt)
    waitTillWritten(filename)
    try:
        command = "pdflatex {}".format(filename)
        print("Executing {}".format(command))
        subprocess.call(shlex.split(command), shell=False)
    except Exception as e:
        print("Failed to execute command")


if __name__ == "__main__":
    usage = '''
This script converts a markdown to another markdown. 
USAGE: ./md2standalone_tikz.py file.md [outfile]

In old file text containing tikzfigures are put into separate tex files inside
standalone environment. A new file is written where tikz text is replaced by
\includegraphics[]{image0.pdf} etc in original file.  Neccessary images are
generated by using pdflatex by this script.
'''

    filename = sys.argv[1]
    try:
        outfile = sys.argv[1]
    except Exception as e:
        outfile = filename.replace("pandoc", "_new.pandoc")

    if not os.path.isfile(filename):
        print("File %s does not exists".format(filename))
        print(usage)
        sys.exit(0)
    txt = open(filename, "r").read()
    txt = extractFigures(txt)
    with open(outfile, "w") as f:
        print("Writing a new file")
        f.write(txt)
    print("DONE")
