#! /usr/bin/python
# -*- coding: utf-8 -*- 

# David Klaper, Carnegie Mellon University

# Script to perform cross validation on a training file
# Usage: python crossValidation.py Train.conll

import sys, os, subprocess, codecs

TMP = "/tmp/"
FOLDCNT = 3
PARSED = os.path.join(TMP, "parse.conll")

def trainParser(trainfile):
    subprocess.call(["./gswDepTrain.py", "--retag", trainfile, os.path.join(TMP, "GSW_foldmodel.model"), "model_type=basic"])
    
    return os.path.join(TMP, "GSW_foldmodel.model")

def parse(reffile, outfile, model):
    subprocess.call(["./gswDepParser.py", "--tagged", reffile, outfile, "--model", model])
    
def evaluate(ref, result):
    subprocess.call(["TurboParser2.1.0/scripts/eval.pl", "-q", "-g", ref, "-s", result])

def writeFiles(folds, testidx):
    trf = os.path.join(TMP, "GSW_train.txt")
    tsf = os.path.join(TMP, "GSW_test.txt")
    with codecs.open(trf, 'w', encoding="utf-8") as train:
        with codecs.open(tsf, 'w', encoding="utf-8") as test:
            for i in range(len(folds)):
                txt = "".join(folds[i])
                if i == testidx:
                    test.write(txt)
                else:
                    train.write(txt)
                
    return trf, tsf

if __name__ == "__main__":
    
    with codecs.open(sys.argv[1], encoding="utf-8") as fline:
        tokens = fline.readlines()
        sentnr = len([k for k in tokens if k.strip() == ""])
    
    foldsize = int(sentnr/float(FOLDCNT))
    
    folds = [[]]
    sen = 0
    for t in tokens:
        if t.strip() == "":
            sen += 1
        
        folds[-1].append(t)
        
        if sen >= foldsize and len(folds) < FOLDCNT:
            sen = 0
            folds.append([])  

    for i in range(FOLDCNT):
        print "Working on Fold", i+1, "out of", FOLDCNT
        (train, test) = writeFiles(folds, i)
        mod = trainParser(train)
        print "Training done:", i+1
        parse(test, PARSED, mod)
        print "Parsing done:", i+1
        evaluate(test, PARSED)
        print "Fold done:", i+1
        
