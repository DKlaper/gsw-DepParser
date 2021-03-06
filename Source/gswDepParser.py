#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper

# Swiss German Parser wrapper usng the underlying TurboParser to parse 
# Swiss-German text

import argparse, os, codecs, subprocess, tempfile, sys
sys.path.append(os.getenv("GSWPARSER", os.getcwd()))

from Settings import * # get settings

import PreProcessing
from Features import FeatureConfig
TURBOP = os.path.join(PARSER, "TurboParser2.1.0","TurboParser")

def argumentSetup():
    """set up the commandline args"""
    parser = argparse.ArgumentParser(description="A Swiss-German dependency parser based on TurboParser")
    
    parser.add_argument('inputFile', help="The input text file, usually a normal text file encoded in utf-8")
    parser.add_argument('outputFile', help="The parsed output CoNLL file encoded in utf-8.")
    parser.add_argument('--model', help="Indicate the model to be used if it is not the default model")
    parser.add_argument('--tagged', action="store_true", help="Indicate to the parser that your data is already in CoNLL format in parsing mode.")
    parser.add_argument('turboOpt', nargs="*", help="Additional options to pass to TurboParser (Without the preceding hyphens: '--evaluate' becomes 'evaluate')")
    
    return parser

if __name__ == "__main__":
    parser = argumentSetup().parse_args()
    taggedFile = parser.inputFile
    # parsing sequence
    if not parser.tagged:
        taggedFile = os.path.join(TEMP, "GSW_tagged"+os.path.basename(parser.inputFile))
        PreProcessing.main(parser.inputFile, taggedFile)
        
    # assign features
    FeatureConfig().run(taggedFile)
        
    model = DEFAULT_MODEL
    if parser.model:
        model = parser.model
        
    # call Turbo Parser
    args = ["--test", "--file_model={}".format(model), "--file_test={}".format(taggedFile), "--file_prediction={}".format(parser.outputFile)]  + map(lambda x: "--"+x, parser.turboOpt)
    
    print "Called TurboParser with options: "+" ".join(args)
        
    subprocess.call([TURBOP]+ args)
    
