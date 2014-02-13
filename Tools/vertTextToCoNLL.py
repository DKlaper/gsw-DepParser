#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Script to tokenize and convert verticalized text into CoNLLX dependency format.
# Usage python TextToCoNLL.py inputTXT outputCoNLL

import sys, codecs, re

sys.stdout = codecs.getwriter("utf-8")(sys.stdout)

if __name__ == "__main__":
    
    with codecs.open(sys.argv[1], encoding="utf-8") as inp:
        inptext = inp.read()
        

    with codecs.open(sys.argv[2], "w", encoding="utf-8") as out:
      cnt = 0
      for line in inptext.split("\n"):
          line = line.strip()
          if line == "":
              out.write("\n") # sentence end need empty line
              cnt = 0
              continue 
          parts = line.split("\t") # Wordform PoS (maybe others e.g. lemma)
          cnt += 1
          out.write(u"{0}\t{1}\t_\t_\t{2}\t_\t{0}\t_\t_\t_\n".format(cnt, parts[0], "NON"))
          
    print "Done", sys.argv[2]
         
