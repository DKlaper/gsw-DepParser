#!/bin/bash

##################################
#Nora Hollenstein
#October 22, 2013
#Swiss german tokenizing and pos-tagging
#Last modified: February 3, 2014
#
#Then
#David Klaper
#February, 6th. 2014
#Only Tokenization!
##################################

#USAGE:
#sh tok_tag_files.sh input_dir/*
#tokenizes all files passed

TOKENIZER="../Source/External/tokenizer/"
OUTPUT_DIR_TOK="../Resources/Wikipedia/"

FILES=$*		##FILES=/path/to/*

x=0
for f in $FILES
do
    echo "Processing $f file..."
    filename=$(basename "$f")
    filename=${filename%.*}
    #tokenizing:
    python ${TOKENIZER}pretok.py $f ${OUTPUT_DIR_TOK}${filename}
    perl ${TOKENIZER}tokenize.pl ${OUTPUT_DIR_TOK}${filename} ${OUTPUT_DIR_TOK}${filename}.tok1
    python ${TOKENIZER}tokenize2.py ${OUTPUT_DIR_TOK}${filename}.tok1 ${TOKENIZER}abbrev.txt
    python ${TOKENIZER}tokenize3.py ${OUTPUT_DIR_TOK}${filename}.tok1 ${TOKENIZER}abbrev.txt
    echo "tokenized."
    
    x=$(($x+1))
done

echo "Tokenized $x files."
# remove intermediate files
#rm ${OUTPUT_DIR_TOK}*[_0-9][0-9]
rm ${OUTPUT_DIR_TOK}*tok1
rm ${OUTPUT_DIR_TOK}*tok2
echo "The tagged files are in the directory ${OUTPUT_DIR_TOK}"
