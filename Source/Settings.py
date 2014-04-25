# -*- coding: utf-8 -*-

# David Klaper, Carnegie Mellon University

# Settings file that sets the parameters for the parser:

import os, tempfile
# Set important paths: (shouldn't need to change these)
TEMP = tempfile.gettempdir()
PARSER = os.getenv("GSWPARSER", os.getcwd())



#####################################################
# SETTINGS (Changing requires retraining of Models!!)
#####################################################

# Set the default TurboParser model:
DEFAULT_MODEL = os.path.join(PARSER,"Models","GSWlowOnlyNEW4P+F+6Stem.model")

# Set the default hunpos model:
POS_MODEL = os.path.join(PARSER, "External", "tagger", "CHDE_57000.model")
# changing this might require retagging your training data!

# Set the default features:
DEFAULTFEATURES = [["BrownCluster", 4], ["BrownCluster", 100], ["PronounciatonStem", 6]]
# currently the only available features are BrownClustering(with prefix length) and PronounciationStem (with prefix length)
# you can implement newfeatures by impementing the Features class (getFeature method) in Features.py

# Set the default clustering:
DEFAULT_CLUSTERING = os.path.join(PARSER, "External", "liang_brownclustering", "clusterings", "defcluster.txt") # this is the C=100 true-cased clustering (and now words that occur less than 3 times)

# Set the default casing:
LOWERCASED = False
if not LOWERCASED:
    CLUSTER_LOOKUP_LOWERCASED = True # look up the word lowercased
    # Consequence if true:  -> clustering true-cased: lowOnly clustering lookup
                        #   -> clustering lower-cased: lower clustering lookup 



