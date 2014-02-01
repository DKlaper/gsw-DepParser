#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Tool to estimate tokens in blogspot xml
#
# Usage python countTokens.py XMLfolder
# estimate tokens of all posts in all xml files in the provided folder

import sys, os, re
from lxml import etree as ET
from collections import defaultdict

if __name__ == "__main__":
    tokens = []
    unique = defaultdict(int)
    totalcount = 0
    # treat all xml files
    for fl in os.listdir(sys.argv[1]):
        if fl.endswith("xml"):
            fullpath = os.path.join(sys.argv[1], fl)
            tree = ET.parse(fullpath)
            tokens = []
            # loop through entries
            for entry in tree.findall("//{*}entry"):
                title = entry.find("{*}title").text
                content = entry.find("{*}content").text
                if title is not None:
                    title = re.sub("<[^>]+>", "", title) # remove html
                    tokens.extend(re.findall(r"\b\w{2,}\b", title, flags=re.I|re.U)) # get tokens  
                
                if content is not None:
                    content = re.sub("<[^>]+>", "", content) # remove html
                    tokens.extend(re.findall(r"\b\w{2,}\b", content, flags=re.I|re.U)) # get tokens  
            
            totalcount += len(tokens)
            for t in tokens:
                unique[t] += 1
            print fl, len(tokens), totalcount

    for topword  in sorted(unique, key=lambda k: unique[k], reverse=True)[:100]:
        print topword, unique[topword]
    print totalcount, len(unique)
