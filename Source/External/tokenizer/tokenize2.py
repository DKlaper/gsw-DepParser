# -*- coding: utf-8 -*-
import re, codecs
import sys

# Nachbearbeitung nach "tokenize.pl" von Frau Stefanie Dipper
# --> ersetzt alle Leerzeichen durch Newline (um vertikalisierten Text zu bekommen)

# Edited by David Klaper

# Aufruf: Name des zu ändernden Files als Argument
file = codecs.open(sys.argv[1], "r", encoding="utf-8").read()
file = re.sub("\n+", "\n\n", file) # preserve sentence boundary
new = re.sub("[^\S\n]+", "\n", file) # replace other white space

# read smiley file to make contract smileys/abbreviations
with codecs.open(sys.argv[2], encoding="utf-8") as smileys:
    reg = "("
    for line in smileys:
        line = line.strip()
        if line == "": # skip empty lines
            continue
        for char in line: # allow token boundary between chars
            if char in r"^$|\()[]?.+{}*": # escaping
                reg += "\\"
            reg += char+r"\n?" 
        reg += "|"
        
    reg = reg[:-1]+")"

# keep smileys together
new = re.sub(reg, lambda m: m.group(1).replace("\n", ""), new, flags=re.U|re.I)

name = sys.argv[1]+".tok2"
outfile = codecs.open(name, "w", encoding="utf-8")
outfile.write(new)

outfile.close()
