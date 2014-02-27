#! /usr/bin/python
# -*- coding: utf-8 -*-

# David Klaper

# Swiss German Parser wrapper usng the underlying TurboParser to parse 
# Swiss-German text

import argparse, os, codecs, subprocess, tempfile, sys

TEMP = tempfile.gettempdir()
# read folder of parser
PARSER = os.getenv("GSWPARSER", os.getcwd())

sys.path.append(PARSER)
import PreProcessing

TURBOP = os.path.join(PARSER, "TurboParser2.1.0","TurboParser")

def argumentSetup():
    """set up the commandline args"""
    parser = argparse.ArgumentParser(description="A Swiss-German dependency parser based on TurboParser")
    
    parser.add_argument('inputFile', help="The input text file, usually a normal text file encoded in utf-8")
    parser.add_argument('outputFile', help="The parsed output CoNLL file encoded in utf-8.")
    parser.add_argument('--model', help="Indicate the model to be used if it is not the default model")
    parser.add_argument('--tagged', action="store_true", help="Indicate to the parser that your data is already in CoNLL format in parsing mode.")
    
    return parser

if __name__ == "__main__":
    parser = argumentSetup().parse_args()
    taggedFile = parser.inputFile
    # parsing sequence
    if not parser.tagged:
        taggedFile = os.path.join(TEMP, "GSW_tagged"+os.path.basename(parser.inputFile))
        PreProcessing.main(parser.inputFile, taggedFile)
        
    model = os.path.join(PARSER,"Models","GSW_original.model")
    if parser.model:
        model = parser.model
        
    # call Turbo Parser
    print model
    args = ["--test", "--file_model={}".format(model), "--file_test={}".format(taggedFile), "--file_prediction={}".format(parser.outputFile), "--logtostderr"]
        
    subprocess.call([TURBOP]+ args)
    
