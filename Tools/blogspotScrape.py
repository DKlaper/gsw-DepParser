#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Tool to download feed xml of a list of blogger/blogspot blogs.
# 
# Usage: python blogspotScrape.py urllistFolder
# where urllistFolder is a folder with .url (Windows) files is
# should be easy to adapt to other formats of the url

import urlparse, urllib2, re, os, codecs
from lxml import etree as ET
from time import sleep

def getBlogSpotId(url):
    """Takes a blogspot url as input and returns the blogid as string"""
    
    requrl = "://".join(urlparse.urlparse(url)[:2]) # baseurl of blog
    
    answerer = urllib2.urlopen(requrl) # go through blog until we find id
    for response in answerer:
        idmatch = re.search('<link rel="service\.post"[^>]+href="[^0-9"]+(\d+)[^"]+"', response,flags=re.I|re.U);
        if idmatch is not None:
            break # close file no need to read whole page
    
    answerer.close()
    sleep(5)
    print "blogid for", requrl, "is", idmatch.groups(1)[0]
    return idmatch.groups(1)[0]

def getBlogSpotXml(blogid, outfile):
    """From the blog id get all blog entries in the blogger atom feed xml"""    
    
    # Request 1: Get number of blog entries
    answerer = urllib2.urlopen("http://www.blogger.com/feeds/{0}/posts/default?max-results=0".format(blogid))
    xmlresp = answerer.read()
    answerer.close()
    
    emptytree = ET.fromstring(xmlresp)
    blogres = emptytree.find("openSearch:totalResults", namespaces={"openSearch":"http://a9.com/-/spec/opensearchrss/1.0/"})
    posts = blogres.text.strip()
    sleep(5)
    # Request 2: Get all blog entris in xml
    print "Getting", posts, "posts from", blogid
    answerer = urllib2.urlopen("http://www.blogger.com/feeds/{0}/posts/default?max-results={1}".format(blogid, posts))
    xmlresp = answerer.read()
    answerer.close()
    
    fulltree = ET.fromstring(xmlresp) # write output
    ET.ElementTree(fulltree).write(outfile, xml_declaration=True, encoding="utf-8", pretty_print=True)
    sleep(5)
    
def readURLfiles(folder):
    """returns a list of urls from the .URL files in the folder (no subfolders)"""
    
    res = []
    for fl in sorted(os.listdir(folder)):
        if fl.endswith("url"):
            with codecs.open(os.path.join(folder, fl)) as urlfl:
                urldat = urlfl.read()
            
            urlmatch = re.search("BASEURL=(\S+)", urldat, flags=re.I|re.U)
            res.append(urlmatch.groups(1)[0])
    
    return res

if __name__ == "__main__":
    
    cnt = 1
    for url in readURLfiles("../Resources/blogURLs"):
        bid = getBlogSpotId(url)
        getBlogSpotXml(bid, "../Resources/blogs/"+urlparse.urlparse(url)[1]+".xml")
        print str(cnt)+"\n*************************************************"
        cnt += 1
