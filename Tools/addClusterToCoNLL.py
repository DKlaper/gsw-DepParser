#! /usr/bin/python
# -*- coding: utf-8 -*- 

# David Klaper, Carnegie Mellon University

# Script to add the cluster number (or transformations of it) as features to the conll file
# python addClusterToCoNLLL.py clustering.txt inputCoNLLfiles...

import sys, codecs

UNK_CLUSTER = "--"

PREFLEN = 4

words = {}
clusters = set()

def readPaths(fl):
    with codecs.open(fl, encoding="utf-8") as fin:
        for line in fin:
            if line.strip() != "":
                parts = line.split()
                words[parts[1]] = parts[0][:PREFLEN]
                clusters.add(parts[0][:PREFLEN])
    return words            
                
if __name__ == "__main__":
    words = readPaths(sys.argv[1])

    for k in sys.argv[2:]:
        text = ""
        with codecs.open(k, encoding="utf-8") as inc:
            for line in inc:
                if line.strip() == "":
                    text += line
                else:
                    parts = line.split("\t")
                    if parts[1] in words:
                        parts[5] = words[parts[1]]
                    else:
                        parts[5] = UNK_CLUSTER
                        
                    text += "\t".join(parts)
                    
        with codecs.open(k, 'w', encoding="utf-8") as out:
            out.write(text)

        print len(clusters)
