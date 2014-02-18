# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Script to add PoS to CoNLL format data.
# Usage python addPoSinCoNLL.py file.conll
# where file.conll is the file that should be enriched

import codecs, subprocess, sys

TAGGEREXE = "Source/External/tagger/hunpos-tag"
ARGS = ["Source/External/tagger/CHDE_57000.model"]

if __name__ == "__main__":
    print sys.argv[1]
    # read data
    data = []
    with codecs.open(sys.argv[1], encoding="utf-8") as inp:
        for line in inp:
            line = line.strip()
            if line == "": # add an element to the split list
                line = "\t"
            data.append(line.split("\t")) # split conll columns
    
    # Pos Tag
    tagger = subprocess.Popen([TAGGEREXE]+ARGS, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=None)
    (res, _) = tagger.communicate(u"\n".join([d[1] for d in data]).encode("utf-8"))

    lines = res.decode("utf-8").split("\n")

    for i, ln in enumerate(lines):
        if len(data) == i:
            break
        parts = ln.strip().split()
        if len(data[i]) > 2:
            #print data[i], parts
            word, tag = parts
            assert data[i][1] == word
            data[i][4]  = tag # 5th column is pos tag
        else:
            #print data[i], parts
            assert len(parts) <= 1 # sentence break
            
    with codecs.open(sys.argv[1], 'w', encoding="utf-8") as out:
        alldat = "\n".join(["\t".join(ln) for ln in data])
        out.write(alldat)
    
