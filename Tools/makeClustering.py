#! /usr/bin/python
# -*- coding: utf-8 -*- 

# David Klaper, Carnegie Mellon University

# Script to turn conll back into flowing text for Clustering
# And then calling the liang clusterer accordingly
# Usage: python makeClustering.py FolderforOutput InputConllFiles...
# it takes as input the output folder and all conll files to be included for training the clusterer

import codecs, subprocess, sys

def makeFile(outfile, fllst):
    with codecs.open(outfile, 'w', encoding="utf-8") as conout:
        
      for fn in fllst:
        text = ""
        if not fn.endswith("conll"):
            continue # skip non conllfiles
        
        with codecs.open(fn, encoding="utf-8") as conin:
            for line in conin:
                #line = line.lower() # lowercased clustering
                if line.strip() == "":
                    text += " \n"
                else:
                    word = line.split("\t")[1]
                    text += word + " "
    
        conout.write(text+" \n")
            
            
if __name__ == "__main__":
    
    makeFile(sys.argv[1], sys.argv[2:])
    
    
