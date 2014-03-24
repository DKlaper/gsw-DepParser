# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Manage the features added to the CoNLL morphological Feature field
# Current available features:
#       - Cluster Number from brown clustering

import os, sys, subprocess, codecs, tempfile
from abc import * # abstract base classes

#DEFAULTFEATURES = [["BrownCluster"], ["BrownCluster", 10]]
DEFAULTFEATURES = [["BrownCluster", 20]]

TEMP = tempfile.gettempdir()
PARSER = os.getenv("GSWPARSER", os.getcwd())

EXTERNALDIR = os.path.join(PARSER, "External/")

UNK_CLUSTER = "--"

class Feature(object):
    """Represent a feature (abstract base class)"""
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getFeature(self, CoNLLWord):
        """Method which passes the current CoNLL line and returns the feature value for this word"""
        return None

class FeatureConfig(object):
    """Class that represents the configuration for the feature field in CONLL"""
    def __init__(self, order=DEFAULTFEATURES):
        """order is a list of lists. Each element list lists the feature to be instantiated and its parameters (as list not dict!!)"""
        # get the own module and search the given class name in this feature module and instantiate that class
        self.featorder = map(lambda k: getattr(sys.modules[self.__module__], k[0])(*k[1:]), order)
        
    def addFeatures(self, conllWord):
        """Add all configured features in the specified order"""
        first = True
        for f in self.featorder:
            assert isinstance(f, Feature) # getFeature must be defined
            if not first:
                conllWord[5] += "|"
            else:
                conllWord[5] = "" # clear feature
                first = False
                
            conllWord[5] += f.getFeature(conllWord)
        
        return conllWord
        
    def run(self, fn):
        with codecs.open(fn, encoding="utf-8") as inp:
            allf = inp.readlines()
            
        with codecs.open(fn, 'w', encoding="utf-8") as out:
            for line in allf:
                parts = line.split("\t")
                if len(parts) > 1:
                    out.write("\t".join(self.addFeatures(parts)))
                else:
                    out.write(line)
        
class BrownCluster(Feature):
    """Class that represents the settings for brownclustering at runtime"""
    def __init__(self, preflen=4, clusteringfile=os.path.join(EXTERNALDIR, "liang_brownclustering", "clusterings", "defclusterLower.txt")):
        self.prefix = preflen
        self.clusters = self.readPaths(clusteringfile)
    
    
    def readPaths(self, fl):
        words = {}
        clusters = set()
        with codecs.open(fl, encoding="utf-8") as fin:
            for line in fin:
                if line.strip() != "":
                    parts = line.split()
                    words[parts[1]] = parts[0][:self.prefix]
                    clusters.add(parts[0][:self.prefix])
        self.clustnr = len(clusters)# find out how many cluster based on chosen prefix length
        return words    
        
    def getFeature(self, CoNLLWord):
        return self.clusters.get( CoNLLWord[1], UNK_CLUSTER)


    
