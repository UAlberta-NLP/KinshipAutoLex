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

#### Codes For Method

This folder contains the implementation of the method described in the paper and a file to evaluate the results.

#### Generating All Concepts
This folder contains a Python file to generate all potential speaker's gender unspecific concepts, and the 2 outputted files: "new_concepts" and "new_relations"

## Operating System
Microsoft Windows 10, Version 10.0.19045.

## Python Version
Python 3.9.12
