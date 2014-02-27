#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper

# Swiss German Parser wrapper usng the underlying TurboParser to parse 
# Swiss-German text

import argparse, os, codecs, subprocess, tempfile, sys

TEMP = tempfile.gettempdir()
# read folder of parser
PARSER = os.getenv("GSWPARSER", os.getcwd())

sys.path.append(PARSER)
TURBOP = os.path.join(PARSER, "TurboParser2.1.0","TurboParser")

def argumentSetup():
    """set up the commandline args"""
    parser = argparse.ArgumentParser(description="Train the Swiss German dependency parser")
    
    parser.add_argument('inputFile', help="The depdency training file in CoNLL format")
    parser.add_argument('outputFile', help="The model trained on the input")
    parser.add_argument('--retag', action="store_true", help="Indicate to the parser that your data should be tagged again before training the model")

    
    return parser
    
def posTag(inpfile, outfile):
    """PoS Tagging on CoNLL file""" 
    TAGGEREXE = os.path.join(PARSER, "External/tagger/hunpos-tag")
    ARGS = [os.path.join(PARSER, "External/tagger/CHDE_57000.model")]
    
    # read data
    data = []
    with codecs.open(inpfile, encoding="utf-8") as inp:
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
            data[i][3]  = tag[0] # 4th column is coarse pos tag
        else:
            #print data[i], parts
            assert len(parts) <= 1 # sentence break
            data[i] = [''] # need to avoid inserting tab at sentence boundary
            
    with codecs.open(outfile, 'w', encoding="utf-8") as out:
        alldat = "\n".join(["\t".join(ln) for ln in data])
        out.write(alldat)

if __name__ == "__main__":
    parser = argumentSetup().parse_args()
    taggedFile = parser.inputFile
    
    # test if we want to tag again
    if parser.retag:
        taggedFile = os.path.join(TEMP, "GSW_tagged"+os.path.basename(parser.inputFile))
        posTag(parser.inputFile, taggedFile)
        
    # call Turbo Parser training
    args = ["--train", "--file_train={}".format(taggedFile), "--file_model={}".format(parser.outputFile),  "--logtostderr"]
    
    subprocess.call([TURBOP]+args)
    
