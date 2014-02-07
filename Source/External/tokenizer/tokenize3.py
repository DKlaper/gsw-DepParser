# -*- coding: utf-8 -*-
import re, codecs
import sys, unicodedata

# Nachbearbeitung nach "tokenize2.py" von Noëmi Apeli
# --> nimmt vertikalisierten Text und trennt Wörter beim Apostroph und bie öffnenden bzw. schliessenden Anführungszeichen

# Edited by David Klaper 

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
for line in file2:
    
    nline = ""
    for (i, char) in enumerate(line):
        if (i != len(line)-1 and line[i+1] != "\n") and (char == "'" or unicodedata.category(char) == "Pi"): # z' laufe  or  " alpha
            nline += char+"\n" # split from rest of word
        elif (i != 0 and line[i-1]!="\n") and unicodedata.category(char) == "Pf":
            nline += "\n"+char
        else: 
            nline += char
    
    nline = re.sub("("+"|".join(smile)+")(\S)", lambda m: m.group(1)+"\n"+m.group(2), nline, flags=re.U|re.I)
    
    nline = re.sub("(\S)("+"|".join(smile)+")", lambda m: m.group(1)+"\n"+m.group(2), nline, flags=re.U|re.I)
    
    outfile2.write(nline)

outfile2.close()
