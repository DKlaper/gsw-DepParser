#!/bin/bash

##################################
#Nora Hollenstein
#October 22, 2013
#Swiss german tokenizing and pos-tagging
#Last modified: February 3, 2014
##################################

#USAGE:
#sh tok_tag_files.sh input_dir/*
#tokenizes and tags all files passed

TOKENIZER="~/tokenizer/"
OUTPUT_DIR_TOK="~/output_tokenizer/"

TAGGER="~/tagger/"
MODEL="~/tagger/54000_jan2014_2"
OUTPUT_DIR_TAG="~/output_tagger/"

#change path for tnt tagger:
TNT="???"

FILES=$*		##FILES=/path/to/*

x=1
for f in $FILES
do
	echo "Processing $f file..."
    filename=$(basename "$f")
    filename=${filename%.*}
    #tokenizing:
    perl ${TOKENIZER}tokenize.pl $f ${OUTPUT_DIR_TOK}${filename}
    python ${TOKENIZER}tokenize2.py ${OUTPUT_DIR_TOK}${filename}
    python ${TOKENIZER}tokenize3.py ${OUTPUT_DIR_TOK}${filename}
    echo "\n\ntokenized.\n\n"
	#pos-tagging:
	${TNT} -v0 ${MODEL} ${OUTPUT_DIR_TOK}${filename}.tok3 > ${OUTPUT_DIR_TAG}${filename}.tagged
    echo "\n\ntagged.\n\n"
    x=$(($x+1))
done

echo "Tokenized and PoS-tagged $x files."
echo "The tagged files are in the directory ${OUTPUT_DIR_TAG}"
