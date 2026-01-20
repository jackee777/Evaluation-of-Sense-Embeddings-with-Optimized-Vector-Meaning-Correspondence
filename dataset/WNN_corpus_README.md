# WNN corpus:
This corpus is a research-oriented corpus created based on ARES (https://nlp.uniroma1.it/sensembert/).
Because ARES is licensed under a Creative Commons Attribution-Noncommercial-Share Alike 4.0 License, this corpus is also licensed under a Creative Commons Attribution-Noncommercial-Share Alike 4.0 License.
However, ARES corpus partially includes BabelNet information. Please read BabelNet's lisence https://babelnet.org/license.

[dataset](https://drive.google.com/file/d/1zBlieyTmNDyeqTyV81rG9C1yPf_2Lwse/view?usp=sharing)

## Citation
If you use this dataset in academic work, please cite both:

```
Yamazaki, T., Ito, S., & Kouzou, Ohara: Evaluation of Sense Embeddings with Optimized Vector-Meaning Correspondence, IEICE TRANSACTIONS on Information and Systems, Vol. E108-D, No. 7, pp. 647--658, 2025.
```
ARES corpus: Scarlini, Bianca and Pasini, Tommaso and Navigli, Roberto: With More Contexts Comes Better Performance: Contextualized Sense Embeddings for All-Round Word Sense Disambiguation, Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing, 2020.

BabelNet, for example: 
Navigli, R., & Ponzetto, S. P. (2012). BabelNet: The automatic construction, evaluation and application of a wide-coverage multilingual semantic network. Artificial Intelligence, 193, 217–250.

---------------------------------------------------------------------------------------------------------
## Overview
// Contents are the same as ReadMe in the base folder.
This folder contains three types of corpus for training word or sense vectors.

## Files
- lemmatized_corpus.txt                 # Non annoated corpus      
- lemmatized_corpus_annoated_synset.txt # Synset annotated corpus

## two example sentences
[lemmatized sentence] 
  he help start the lutheran school and seminary at altenburg , which be function by 1841 and possibly as early as 1839 .
[Synset annotated sentence] # Partial annotation
  he help start the lutheran#bn:00052385n school and seminary at altenburg , which be function by 1841 and possibly as early as 1839 .

[lemmatized sentence] 
  during one of he peep session , gōda witness the murder of one of the tenant at the hand of lady minako .
[Synset annotated sentence] # Partial annotation
  during one of he peep#bn:00091516v session , gōda witness the murder of one of the tenant at the hand of lady minako .     
