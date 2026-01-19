# WNN dataset:
This dataset is a research-oriented dataset created based on BabelNet, a multilingual semantic network integrating heterogeneous lexical and encyclopedic resources.

The dataset is intended exclusively for academic and research purposes and is distributed in compliance with the BabelNet Non-Commercial License. 

If you want to get the dataset, please contact the first author.

---------------------------------------------------------------------------------------------------------
## Terms of Use

All copyrights to the Data are owned by the copyright holder(s) stated in the space for names of copyright holder(s). Users may reproduce and use the Data freely in accordance with the following terms and conditions.

1) No guarantee of a certain functionality or objective is made for the Data. Accordingly, Users shall consent to the use of the Data under their own responsibility.

2) The Data is provided to Users free of charge, and neither copyright holder(s) nor the Institute of Electronics, Information and Communication Engineers assume any obligation to guarantee for direct or indirect loss or loss due to the ripple effect, damage to data and programs, or other intangible property rights, loss of profits through use or unrealized profits arising from use of the Data.

3) All persons who are not copyright holder(s) of the Data are prohibited from publishing the Data without permission.

4) The Data can be used for Research Purposes only and for no other purpose.

5) The use of this dataset always requires referencing the WordNet and BabelNet authorities.

WordNet 3.0 Copyright 2006 by Princeton University. 

All rights reserved. THIS SOFTWARE AND DATABASE IS PROVIDED "AS IS" AND PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED. BY WAY OF EXAMPLE, BUT NOT LIMITATION, PRINCETON UNIVERSITY MAKES NO REPRESENTATIONS OR WARRANTIES OF MERCHANT- ABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE LICENSED SOFTWARE, DATABASE OR DOCUMENTATION WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS. 

This data is a processed version of BabelNet v5.0 downloaded from https://babelnet.org, made available with the BabelNet Non-Commercial License (see https://babelnet.org/full-license).

Please read BabelNet's lisence https://babelnet.org/license.

[Citation]
If you use this dataset in academic work, please cite both:
This dataset:
Yamazaki, T., Ito, S., & Kouzou, Ohara: Evaluation of Sense Embeddings with Optimized Vector-Meaning Correspondence, IEICE TRANSACTIONS on Information and Systems, Vol. E108-D, No. 7, pp. 647--658, 2025.
BabelNet, for example:
Navigli, R., & Ponzetto, S. P. (2012). BabelNet: The automatic construction, evaluation and application of a wide-coverage multilingual semantic network. Artificial Intelligence, 193, 217–250.


---------------------------------------------------------------------------------------------------------
[Overview]
WNN-ARES is a dataset containing only the meanings contained in the training corpus and WNN-ALL is a dataset containing all available meanings in concept hierarchies. For the same reason, similar words are limited in WNN-ARES. Moreover, in WNN-ARES, the word ``motel'' is removed due to its low frequency of occurrence in the training corpus.

- WNN-ARES  # Dataset containing only the meanings contained in the training corpus. 

## Files
./                                   
|-- WNN-ARES      # Dataset containing only the meanings contained in the training corpus. 
|    |-- *.csv    # 498 (word) files. ``motel'' is removed due to its low occurrence in corpus.

## CSV Format
In each file, the number of rows means the number of meanings of a word in the dataset and there are nine columns: word, PoS, synsets, synonyms, siblings, hypernyms-1, hypernyms-2, hyponyms-1, and hyponyms-2.

- word: a target word in evaluation
- PoS: Part-of-Speech
- synsets (synset IDs): A synset ID consists of three kinds of information: an abbre-viation of the respective concept hierarchy (wn: WordNet,bn: BabelNet), ID (an eight-digit number), and the first letterof the PoS (n: noun, v: verb).
- similar words: synonyms, siblings, hypernyms-1, hypernyms-2, hyponyms-1, and hyponyms-2.

#### an example of lemon
word    | PoS  |      synsets      |     synonyms    |     siblings    |  hypernyms-1  | ...
lemon   | Noun | wn:07749582n, ... |        -        |    lime, ....   |  citrus, ...  | ...
lemon   | Noun | wn:04966543n, ... |   gamboge, ...  |   golden, ...   |  yellow, ...  | ...
lemon   | Noun | wn:12711596n, ... | lemon_tree, ... |kumquat_tree, ...|  citrus, ...  | ...
lemon   | Noun | wn:03655838n, ... |   stinker, ...  |  squeaker, ...  | artifact, ... | ...
                ----- WNN-ALL contains another meaning, as follows. -----
lemon   | Noun | wn:05716342n, ... |        -        |     vanilla     |  flavour, ... | ...
// This order is different from the actual order for the viewing. 
