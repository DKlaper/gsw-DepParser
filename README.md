gsw-DepParser
=============

A dependency parser for Swiss-German (ISO 639 code: gsw) by David Klaper

Installation
============

All relative paths, are relative to the folder that contains this readme.

Copy the repository
Download the tokenizer.pl from
http://www.linguistics.ruhr-uni-bochum.de/~dipper/tokenizer.html#download
and place in the Source/External/tokenizer.

Then if necessary recompile turbo parser by going to Source/TurboParser2.1.0
and executing ./install-deps.sh
and ./configure && make && make install

Optional: 
Set the environment variable GSWPARSER to the path to the Source/ folder
and also add the path to Source/ to your PATH.
(this sets all the relative paths correctly if you call the parser from somewhere else
by typing gswDepParser.py (without python))

Basic Usage
===========

Execute all commands in the Source/ folder    (OR if you set GSWPARSER to Source and added GSWPARSER to your path execute the commands without writing python in any folder you want but the paths to the Models will be different.)


To parse: 
python gswDepParser.py  --model Models/parsingmodel input.txt output.predicted

if your input is in CoNLL
python gswDepParser.py  --tagged --model Models/parsingmodel input.conll output.predicted

You don't need to use the --model option, then just the standard model describe in the report as LowOnly C100 4P+F+6Stem normal will be used. (for more options just call the programs without arguments)



To train a parser:
python gswDepTrain.py train.conll Models/outparsingmodel model_type=basic

model_type=basic is an option directly for turbo parser training only a basic model, you can also train other model_types
or remove the option. Then a standard model will be trained.

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

Advanced Usage
=================================

CHANGE FEATURE SETTINGS

Go to Source/Settings.py and change the corresponding values to change settings of the parser.
NOTE that this may require retraining of the model to have the desired effect! 
To change the features present in the CoNLL feature column change 
DEFAULTFEATURES = [["BrownCluster", 4], ["BrownCluster", 100], ["PronounciatonStem", 6]]

This takes a brown cluster prefix of 4 then one with the full string (prefix = 100 is full string with C=100)
and the pronunciation normalization with a 6 character prefix. So you can change the number of features by adding and removing entries, as well as the prefix lengths. 

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

if you rename the clustering file be sure to change the setting in Source/Settings.py, in particular DEFAULT_CLUSTERING.

Licenses Tokenizer, Tagger
==========================

This parser, i.e., the python scripts + the training material (But not external tools such as the tokenizer and clusterer!!) are licensed under the Apache 2.0 license

Copyright 2014 David Klaper, Carnegie Mellon University

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
