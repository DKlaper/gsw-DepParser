# -*- coding: utf-8 -*-

# David Klaper
#
# Script to tokenize blogspots with missing whitespace between words

import re, codecs
import sys

class Cleaner(object):
    def __init__(self):
        """Compile regular expressions and replacements"""
        self.re = []
        # cases like han.Ich
        sepW = (re.compile(ur"([^\W\d])([\!\?\.#%&*,.:;|]+)([^\W\d_])", flags=re.U|re.I), lambda m: m.group(1)+" "+m.group(2)+" "+m.group(3) )
        # cases like han....
        sepW2 = (re.compile(ur"([^\W\d])([\!\?\.#%&*,.:;|]+)", flags=re.U|re.I), lambda m: m.group(1)+" "+m.group(2) )
        
        # don't do ...han, because of smileys?  :D -> : D
        self.re.extend([sepW, sepW2])
        
        
    def clean(self, text):
        """clean the text"""
        for r in self.re:
            text = r[0].sub(r[1], text)
            
        return text

out = codecs.open(sys.argv[2], 'w', encoding="utf-8")
clean = Cleaner()

with codecs.open(sys.argv[1], encoding="utf-8") as inp:
    for line in inp:
        line = clean.clean(line)
        out.write(line)
    

out.close()
