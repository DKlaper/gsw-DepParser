#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Script to count tokens of blog posts files
#
# Usage: python countTxtTokens.py folder
# where folder is the folder that contains the txt files with the blogposts

from nltk import wordpunct_tokenize
from collections import defaultdict
import os, sys, codecs, re

if __name__ == "__main__":
    
    tokencount = 0
    typecount = defaultdict(int)
    
    folder = sys.argv[1]
    for fl in os.listdir(folder):
        tokens = []
        if fl.endswith(".txt"):
            
            with codecs.open(os.path.join(folder, fl), encoding="utf-8") as txt:
                tokens = re.findall(r"\b\w{2,}\b", txt.read(), flags=re.I|re.U)#wordpunct_tokenize(txt.read())
            
            for t in tokens:
                tokencount += 1
                typecount[t] += 1
                
                
    for topword in sorted(typecount, key=lambda k: typecount[k], reverse=True)[:100]:
        print topword, typecount[topword]
    print "Tokens", tokencount, "Types",len(typecount), "Hapax legonoma", len([x for x in typecount if typecount[x] == 1])
