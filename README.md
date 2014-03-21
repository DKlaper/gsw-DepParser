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

Basic Usage
===========

Execute in the Source/ folder
To parse: 
python gswDepParser.py  --model Models/parsingmodel input.txt output.predicted

if your input is in CoNLL
python gswDepParser.py  --tagged --model Models/parsingmodel input.conll output.predicted


To train a parser:
python gswDepTrain.py train.conll Models/outparsingmodel model_type=basic

model_type=basic is an option directly for turbo parser training only a basic model, you can also train other model_types
or leave the option out. Then a standard model will be trained.

(for more options just call the programs without arguments)


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

Advanced Usage: Clustering
=================================

CHANGE FEATURE SETTINGS

to change the feature settings go to Source/Features.py
and change DEFAULTFEATURES = [["BrownCluster"], ["BrownCluster", 10]]
each list element is a feature the format is ["Feature name", arg1, arg2]
for BrownCluster it is  ["BrownCluster", prefixLength, clusterfilepath]

CREATE NEW CLUSTERING

To create a clustering you can perform the following steps from this Folder:

To create normally flowed text in complete.txt from the CoNLL files:
python Tools/makeClustering.py Resources/ClusteringData/complete.txt Resources/ClusteringData/*.conll 

Then run the clustering on this file: 
Source/External/liang_brownclustering/wcluster --c 100 --min-occur 3 --text Resources/ClusteringData/complete.txt --paths Source/External/liang_brownclustering/clusterings/defcluster.txt --output_dir /tmp/clustering

--c is the number of clusters
--min-occur is how many times a word has to occur in the corpus to be considered
--text is the input
--paths is the clustering file
--output_dir is for additional files like logs that you typically don't need just for parsing
(Assuming you have compiled the clusterer by calling make in the Source/External/liang_brownclustering/ Folder)

if you rename the clustering file be sure to call the appropriate file in the DEFAULTSETTINGS in Source/Features.py as second argument to BrownCluster

Licenses Tokenizer, Tagger
==========================

This parser, i.e., the python scripts + the training material are licensed under the Apache 2.0 license

Copyright 2014 David Klaper

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.



NOTE that some external parts of this software cannot be used for commercial/non-research purposes:
If you want to use the parser for commercial purposes you have to replace in particular the clusterer and the tokenizer.
Please consult the relevant licenses

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
