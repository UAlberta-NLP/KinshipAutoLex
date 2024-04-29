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
<div>
<textarea id="copyText" style="width:100%;height:100px;">
This is the text that will be copied.
</textarea>
<button onclick="copyFunction()">Copy Text</button>
</div>

<script>
function copyFunction() {
  var copyText = document.getElementById("copyText");
  copyText.select();
  document.execCommand("copy");
}
</script>

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
> This code requiring one additional package, googletrans==3.1.0a0, which can be installed by pip:
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

##### evaluate_cleaned_version.py
This file contains the code to evaluate the results outputted by "goolge_trans_method_cleaned.py".

The output of this code is the Acc of LexGen and F1 Score of LexGap. 
 
This file takes 1 argument.

-l takes a string input that indicates the target language.

The default target language is English.

Sample run: python evaluate_cleaned_version.py -l English




### Generating All Concepts
This folder contains a Python file to generate all potential speaker's gender unspecific concepts, and the 2 outputted files are: "new_concepts" and "new_relations"
The files in this folder allow you to generate the results we reported in Table 2.

## Operating System
Microsoft Windows 10, Version 10.0.19045.

## Python Version
Python 3.9.12
