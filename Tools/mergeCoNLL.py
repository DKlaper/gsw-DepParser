# -*- coding: utf-8 -*-

# David Klaper

# Merge different CoNLL files to make one big training or test file

# Usage:
# python mergeCoNLL.py input1 input2 ....
# all inputs are in CoNLL, output is to stdout

import sys, codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

if __name__ == "__main__":
    for fl in sys.argv[1:]:
        with codecs.open(fl, encoding="utf-8") as inp:
            
            for line in inp:
                sys.stdout.write(line)
                
            sys.stdout.write("\n")
