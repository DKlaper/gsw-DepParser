# -*- coding: utf-8 -*-
import re, codecs
import sys, unicodedata

# Nachbearbeitung nach "tokenize2.py" von Noëmi Apeli
# --> nimmt vertikalisierten Text und trennt Wörter beim Apostroph und bie öffnenden bzw. schliessenden Anführungszeichen

# Edited by David Klaper 

# class to manage state of sentence end detection
class Sentence(object):
    def __init__(self):
        self.tokens = 0
        self.clean = True # no word seen yet in sentence 
        self.inSentence = "^[^.!?]+" # regex to describe what is allowed to be next token in sentence
        self.word = "^\w+"
        self.endpending = False # if we have seen final punctuation
        
    def reset(self):
        self.tokens = 0
        self.newlines = 0
        self.endpending = False
        self.clean = True
        
    def processTokens(self, line):
        """returns true if sentence end, false if not and none if item has to be deleted -> too many empty lines"""
        if line.strip() == "":
            if sen.clean: # an empty line after another empty line
                return None
            self.reset() # found sentence end
            return False
        self.newlines = 0
        self.clean = False
        mtc = re.match(self.inSentence, line)
        self.tokens += 1
        if (not mtc) and self.tokens > 3: # found sentence End
            self.endpending = True
            return False
        else:
            if re.match(self.word, line, flags=re.U|re.I):
                if self.endpending:
                    self.reset()
                    return True
                else:
                    return False
            else: # punctuation and similar things attached
                return False
                
        

# smileys
# read smiley file to split smiley
with codecs.open(sys.argv[2], encoding="utf-8") as smileys:
    smile = []
    for line in smileys:
        line = line.strip()
        nline = ""
        for char in line: 
            if char in r"^$|\()[]?.+{}*":
                nline += "\\"
            nline += char
        
        smile.append(nline)

outfile2 = codecs.open(sys.argv[1]+".tok3", "w", encoding="utf-8")
file2 = codecs.open(sys.argv[1]+".tok2", 'r', encoding="utf-8").readlines()
sen = Sentence()
for line in file2:
    
    nline = ""
    for (i, char) in enumerate(line):
        if (i != len(line)-1 and line[i+1] != "\n") and (char == "'" or unicodedata.category(char) == "Pi"): # z' laufe  or  " alpha
            nline += char+"\n" # split from rest of word
        elif (i != 0 and line[i-1]!="\n") and unicodedata.category(char) == "Pf": # separate closing characters
            nline += "\n"+char
        else: 
            nline += char
    
    nline = re.sub("("+"|".join(smile)+")(\S)", lambda m: m.group(1)+"\n"+m.group(2), nline, flags=re.U|re.I)
    
    nline = re.sub("(\S)("+"|".join(smile)+")", lambda m: m.group(1)+"\n"+m.group(2), nline, flags=re.U|re.I)
    
    # check sentence end state 
    parts = nline.splitlines(True)
    nline = ""
    for p in parts:
        val = sen.processTokens(p)
        if val is None: # redundant empty line at sentence end
            assert nline.strip() == ""
            continue
        elif val: # sentence end before token
            p = "\n"+p
        
        nline += p
    
    outfile2.write(nline)

outfile2.close()
