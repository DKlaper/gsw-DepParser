gsw-DepParser
=============

A dependency parser for Swiss-German (ISO 639 code: gsw)

Installation
============

Currently just copy Repo
download the tokenizer from
http://www.linguistics.ruhr-uni-bochum.de/~dipper/tokenizer.html#download
and place in the Source/External/tokenizer.

Then Recompile turbo parser by going to Source/TurboParser2.1.0
and executing ./install-deps.sh
and ./configure && make && make install

Optionally set the environment variable GSWPARSER to the path to the Source/ folder
and also add the path to Source/ to your PATH.
(this sets all the relative paths correctly if you call the parser from somewhere else
by typing gswDepParser.py (without python))

Organization of the Repo
========================

- Literature
    contains pdfs of the most important references.
    
- Report 
    contains the latex source and pdf of the report. It contains valuable
    information about the project
    
- Resources
    contains the data (i.e., blog sources, blog tokenized,
    annotated training and test data with automatically assigned PoS tags)
    Look at the explanation file to know more about the contents.
    
- Source
    contains the source code of the parser and Source/External/ contains the tokenizer and tagger.
    The main executables are gswDepTrain.py to train and gswDepParser.py to parse a file
    
    Note that the tokenizer (tokenize.pl) MUST be downloaded from 
    http://www.linguistics.ruhr-uni-bochum.de/~dipper/tokenizer.html#download
    and placed in the Source/External/tokenizer.
    
- Tools
    contains script to extract blogs from blogspot and deal with the atom xml format.
    Look at the explanation file to know more about the contents.

Requirements and Assumptions
============================

This parser requires:
    python (2.7)
    perl   (5 v14)
    
It assumes that input is utf-8 encoded and uses "\n" (Unix) line endings

Licenses Tokenizer, Tagger
==========================

The PoS-Tagger HunPos is distributed under the new BSD license http://opensource.org/licenses/BSD-3-Clause
For more information visit their website at http://code.google.com/p/hunpos/
The CHDE_57000.model for hunpos is courtesy of Nora Hollenstein and Noëmi Aepli from the 
University of Zurich.
It may be reused unchanged in the hunpos tagger and the authors need to be attributed.

The tokenizer is licensed under a custom non-commercial, non-distribution license.
It can be found here: http://www.linguistics.ruhr-uni-bochum.de/~dipper/licence.txt

The Turbo Parser v2.1.0 is licensed under the GNU lesser general public license v3.0

Percy Liang's Brown Clustering algorithm is licensed under a custom education/research only license.
You can find the license at the end of the readme in Source/External/liang_brownclustering/
