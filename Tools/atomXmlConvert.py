#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Script to extract the relevant blogtext into a more convenient format
#
# Usage: python atomXmlConvert.py inputfolder outputfolder
# convert the ATOM inputfiles into textfiles (one per blogpost). 

from lxml import etree as ET
from htmlentitydefs import name2codepoint
import sys, codecs, re, os

# set stdout encoding
sys.stdout = codecs.getwriter("utf-8")(sys.stdout) 

def htmlunescape(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint),
            lambda m: unichr(name2codepoint[m.group(1)]), s)

class Blog(object):
    def __init__(self):
        self.posts = []
        
class Post(object):
    def __init__(self, xmlentry):
        self.text = Post.toText(xmlentry)
        self.xml = xmlentry
        
    @classmethod
    def toText(cls, xmlentry):
        text = ""
        title = entry.find("{*}title").text
        content = entry.find("{*}content").text
        if title is not None:
            text += title+"\n\n"
        if content is not None:
            text += content
        text = Post.clean(text)
        return text
    
    @classmethod
    def clean(cls, text):
        text = text.replace("&nbsp;", " ") # make a normal space
        text = text.replace(u"\uFEFF", "") # zerowidth space
        text = htmlunescape(text) # build html entities
        text = re.sub("(<br\s*/?>)", "\n", text) # use breaks as newlines
        text = re.sub("<img[^><]+>", "\n", text) # mark images as breaks
        text = re.sub("<[^><]+>", "", text) # remove tags
        return text
        

if __name__ == "__main__":
    
    filecnt = [0,0] # count blog count + post count
    for fl in sorted(os.listdir(sys.argv[1])):
        if not fl.endswith("xml"):
            continue
        filecnt[0] += 1 # increment blog count
        filecnt[1] = 0 # reset post count
        tree = ET.parse(os.path.join(sys.argv[1], fl))
        for entry in tree.findall("//{*}entry"):
            post = Post(entry)
            if post.text.strip() == "": # no need to write empty files
                continue
            filecnt[1] += 1 # increment post count
            with codecs.open(os.path.join(sys.argv[2], "blog_{0}_{1}.txt".format(*filecnt)), "w", encoding="utf-8") as outfile:
                outfile.write(post.text) 
                
        print fl, filecnt
        
