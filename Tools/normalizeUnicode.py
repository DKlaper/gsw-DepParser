#! /usr/bin/python
# -*- coding: utf-8 -*- 

# David Klaper, Carnegie Mellon University

# Script which just takes each file and replaces it by assuming it's utf-8 and normalizing it into NFC
# canonical composition normal form
# Usage: python file1.txt [file2.txt, file3.txt, ...]

import codecs, unicodedata, sys

if __name__ == "__main__":
    for f in sys.argv[1:]:
        with codecs.open(f, encoding="utf-8") as inp:
            text = inp.read()
            
        text = unicodedata.normalize("NFC", text)
        
        with codecs.open(f, 'w', encoding="utf-8") as out:
            out.write(text)
