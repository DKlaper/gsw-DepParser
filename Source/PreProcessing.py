# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Wrapper that takes an input text and runs tokenization and PoS-tagging on it
# Furthermore the output is in CoNLL format

# Standalone Usage
# python PreProcessing.py inputFile outputFile

import os, sys, subprocess, codecs, tempfile

TEMP = tempfile.gettempdir()
PARSER = os.getenv("GSWPARSER", os.getcwd())

EXTERNALDIR = os.path.join(PARSER, "External/")

def preTagProc(word):
    """Preprocessing before tagging"""
    
    # tagger tags almost everything as NE if it's in capitals
    if len(word) > 1 and word.isupper():
        word = word.lower()
        
    return word

def preParseProc(word, tag):
    """Preprocessing before parsing (after tagging)"""
    # lowercase everything? 
    #word = word.lower()
     
    
    return word, tag

def tokenize(filepath):
    """Call the tokenizer, write to filepath.tokenized. Will raise an Exception if any call fails.
    Returns the path to the tokenized file"""

    fn = os.path.basename(filepath)
    outpth = os.path.join(TEMP, "GSW_3_"+fn) #filepath+".tokenized"
    # pretokenization
    subprocess.check_call(["python", os.path.join(EXTERNALDIR,"tokenizer", "pretok.py"), filepath, os.path.join(TEMP, "GSW_1_"+fn)]) 
    # main tokenization
    subprocess.check_call(["perl", os.path.join(EXTERNALDIR,"tokenizer", "tokenize.pl"), os.path.join(TEMP, "GSW_1_"+fn), os.path.join(TEMP, "GSW_2_"+fn)])
    # post tokenization
    subprocess.check_call(["python", os.path.join(EXTERNALDIR,"tokenizer", "tokenize2.py"), os.path.join(TEMP, "GSW_2_"+fn), os.path.join(EXTERNALDIR,"tokenizer", "abbrev.txt")])
    subprocess.check_call(["python", os.path.join(EXTERNALDIR,"tokenizer", "tokenize3.py"), os.path.join(TEMP, "GSW_2_"+fn), os.path.join(EXTERNALDIR,"tokenizer", "abbrev.txt")])
    
    os.rename(os.path.join(TEMP, "GSW_2_"+fn+".tok3"), outpth)
    subprocess.call(["rm "+ os.path.join(TEMP, "GSW_[1-2]_*"+fn+"*")], shell=True)
    
    return outpth

def PoStag(filepath, output, postProc=lambda w, tag: (w,tag), preProc=lambda w: w):
    """Pass tokenized file to tagger convert file to CoNLL and write to output"""
    
    inpt = codecs.open(filepath, encoding="utf-8")
    text = inpt.readlines()
    inpt.close()
    
    text = "\n".join([preProc(w.strip()) for w in text])
    
    tagger = subprocess.Popen([os.path.join(EXTERNALDIR, "tagger", "hunpos-tag"), os.path.join(EXTERNALDIR, "tagger", "CHDE_57000.model")], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
            parts[0], parts[1] = postProc(parts[0], parts[1]) # post process tag
            res += u"{}\t{}\t_\t{}\t{}\t_\t{}\t_\t_\t_\n".format(i, parts[0], parts[1][0], parts[1], i)
            i+= 1
    
    with codecs.open(output, 'w', encoding="utf-8") as out:
        out.write(res)
    
    return res
            
def main(arg1, arg2):
    PoStag(tokenize(arg1), arg2, preProc=preTagProc, postProc=preParseProc).encode("utf-8", errors="xmlcharrefreplace")
    
if __name__ == "__main__":
    main(*sys.argv[1:])
