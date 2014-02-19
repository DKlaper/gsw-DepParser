# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Wrapper that takes an input text and runs tokenization and PoS-tagging on it
# Furthermore the output is in CoNLL format
# By default -> lowercase everything

# python PreProcessing.py inputFile outputFile

import os, sys, subprocess, codecs

TEMPDIR = "/tmp/"
EXTERNALDIR = "External/"
SUFFIX = "tokenized"

# allow calling the parser from other CWDs later
if os.getenv("GSWparser"):
    EXTERNALDIR = os.getenv("GSWparser")+EXTERNALDIR


def tokenize(filepath):
    """Call the tokenizer, write to filepath.tokenized. Will raise an Exception if any call fails.
    Returns the path to the tokenized file"""

    fn = os.path.basename(filepath)
    outpth = os.path.join(TEMPDIR, "GSW_3_"+fn) #filepath+".tokenized"
    # pretokenization
    subprocess.check_call(["python", os.path.join(EXTERNALDIR,"tokenizer/pretok.py"), filepath, os.path.join(TEMPDIR, "GSW_1_"+fn)]) 
    # main tokenization
    subprocess.check_call(["perl", os.path.join(EXTERNALDIR,"tokenizer/tokenize.pl"), os.path.join(TEMPDIR, "GSW_1_"+fn), os.path.join(TEMPDIR, "GSW_2_"+fn)])
    # post tokenization
    subprocess.check_call(["python", os.path.join(EXTERNALDIR,"tokenizer/tokenize2.py"), os.path.join(TEMPDIR, "GSW_2_"+fn), os.path.join(EXTERNALDIR,"tokenizer/abbrev.txt")])
    subprocess.check_call(["python", os.path.join(EXTERNALDIR,"tokenizer/tokenize3.py"), os.path.join(TEMPDIR, "GSW_2_"+fn), os.path.join(EXTERNALDIR,"tokenizer/abbrev.txt")])
    
    os.rename(os.path.join(TEMPDIR, "GSW_2_"+fn+".tok3"), outpth)
    subprocess.call(["rm "+ os.path.join(TEMPDIR, "GSW_[1-2]_*"+fn+"*")], shell=True)
    
    return outpth

def PoStag(filepath, output, postProc=lambda tag,w: tag, preProc=lambda w: w):
    """Pass tokenized file to tagger convert file to CoNLL and write to output"""
    
    inpt = codecs.open(filepath, encoding="utf-8")
    text = inpt.readlines()
    inpt.close()
    
    text = "\n".join([preProc(w.strip()) for w in text])
    
    tagger = subprocess.Popen([os.path.join(EXTERNALDIR, "tagger/hunpos-tag"), os.path.join(EXTERNALDIR, "tagger/CHDE_57000.model")], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # pipe to input
    (lines, _) = tagger.communicate(text.encode("utf-8"))
    
    res = ""
    i = 1
    for ln in lines.split("\n"):
        ln = ln.strip().decode("utf-8")
        if ln == "":     # was sentence break
            i = 1
            res += "\n"
        else:
            parts = ln.rsplit(None,1) # support multiword tokens
            res += u"{}\t{}\t_\t{}\t{}\t_\t{}\t_\t_\t_\n".format(i, parts[0], postProc(parts[1], parts[0]), parts[1], i)
            i+= 1
    
    #with codecs.open(output, 'w', encoding="utf-8") as out:
    #    out.write(res)
    
    return res
    
            
if __name__ == "__main__":
    
    print PoStag(tokenize(sys.argv[1]), sys.argv[2], preProc=lambda w: w).encode("utf-8", errors="xmlcharrefreplace"),
    
