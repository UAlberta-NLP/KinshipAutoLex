# KinshipAutoLex
This repository is for the paper Translation-based Lexicalization Generation and Lexical Gap Detection: Application to Kinship Terms.

## Paper Information

#### Title
Translation-based Lexicalization Generation and Lexical Gap Detection: Application to Kinship Terms.

#### Year of publication
Under Review

#### Track of publication

Under Review

#### Authors

Senyu Li, Bradley Hauer, Ning Shi, Grzegorz Kondrak

#### Abstract
Constructing lexicons with explicitly identified lexical gaps is a vital part of building multilingual lexical resources.
Prior work has leveraged bilingual dictionaries and linguistic typologies for semi-automatic identification of lexical gaps. 
Instead, we propose a generally-applicable algorithmic method 
to automatically generate concept lexicalizations,
which is based on machine translation 
and hypernymy relations between concepts.
The absence of a lexicalization implies a lexical gap. 
We apply our method to kinship terms, 
which make a suitable case study 
because of their explicit definitions and regular structure. 
Empirical evaluations demonstrate that our approach 
yields higher accuracy than
BabelNet
and ChatGPT. 
Our error analysis indicates 
that enhancing the quality of translations 
can further improve the accuracy of our method.

## Codes

### Codes For Method

This folder contains the implementation of the method described in the paper and a file to evaluate the results.
The files in this folder allow you to replicate the experiment in Section 5 of our paper, to generate the results we reported in Table 3.
#### Codes contained
##### goolge_trans_method_cleaned.py
> This file contains the implementation of the method described in section 4 of the paper, in which the used translator is Google Translate.
> 
> The output of this code is a ".txt" file in the "Results" folder.
> 
> This code requires one additional package other than the default packages, googletrans==3.1.0a0
> 
> This file takes 3 arguments.
> 
> -l takes a string input that indicates the target language of this run
> 
> -t takes a boolean input that indicates whether to use the prepared set of translations in the folder "Translation".
> 
> -b takes a boolean input that indicates whether to use the prepared set of results of back translations in the folder "Translation".
> 
> The default target language is English, and the prepared translation and back-translation results will are not used by default.

> Sample run: python goolge_trans_method_cleaned.py -l English -t True -b True
> 
> To replicate the results on the 13 languages we reported on the paper, other than the command in the sample run, 12 more commands are needed, one for each remaining language.
> The remaining commands can be made by replacing "English" with the target language.
> 
> We reported our results on English, Spanish,	Russian,	French,	German,	Mandarin,	Persian,	Polish,	Arabic,	Italian,	Mongolian,	Hungarian and Hindi.   


##### evaluate_cleaned_version.py
>This file contains the code to evaluate the results outputted by "goolge_trans_method_cleaned.py".
>
>The output of this code is the Acc of LexGen and F1 Score of LexGap. 
> 
>This file takes 1 argument.
>
>-l takes a string input that indicates the target language.
>
>The default target language is English.

>Sample run: python evaluate_cleaned_version.py -l English
>
>To evaluate the results on other languages, replace "English" in the sample run with the target language you want.




### Generating All Concepts
This folder contains a Python file to generate all potential speaker's gender-unspecific concepts.
The files in this folder allow you to generate the results we reported in Table 2.

#### generating_all_concepts_edges.py
>The Python file to generate all potential speaker's gender-unspecific concepts, and the 2 outputted files are: "new_concepts" and "new_relations"
>
>This file can be run directly.
>
>Sample run: python generating_all_concepts_edges.py

>The outputted file "new_concepts" contains 3 columns: The subdomain of the concept, the newly generated concept name for the concept, and the abbr name of the concept.
>
>The outputted file "new_relations" contains 3 columns: The subdomain of this edge,  the abbr name of the hyponym concept, and the abbr name of the hypernym concept.

## Operating System
Microsoft Windows 10, Version 10.0.19045.

## Python Version
Python 3.9.12
