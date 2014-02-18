gsw-DepParser
=============

A dependency parser for Swiss-German (ISO 639 code: gsw)


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
    
    Note that the tokenizer (tokenize.pl) MUST be downloaded from 
    http://www.linguistics.ruhr-uni-bochum.de/~dipper/tokenizer.html#download
    and placed in the Source/External/tokenizer.
    
- Tools
    contains script to extract blogs from blogspot and deal with the atom xml format.
    Look at the explanation file to know more about the contents.

Licenses Tokenizer, Tagger
==========================

    The PoS-Tagger HunPos is distributed under the new BSD license http://opensource.org/licenses/BSD-3-Clause
    For more information visit their website at http://code.google.com/p/hunpos/
    The CHDE_57000.model is courtesy of Nora Hollenstein and Noëmi Aepli.
    It may be reused unchanged in the hunpos tagger and the authors need to be attributed.
    
    The tokenizer is licensed under a custom non-commercial, non-distribution license.
    It can be found here: http://www.linguistics.ruhr-uni-bochum.de/~dipper/licence.txt
