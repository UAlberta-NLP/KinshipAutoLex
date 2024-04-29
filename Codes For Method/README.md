# Codes For Method
This folder contains the implementation of the method described in the paper and a file to evaluate the results.

# goolge_trans_method_cleaned.py
This file contains the implementation of the method, in which the used translator is Google Translate.

The output of this code is a ".txt" file in the "Results" folder.

Required additional package: googletrans==3.1.0a0

This file takes 3 arguments.

-l takes a string input that indicates the target language of this run

-t takes a boolean input that indicates whether to use the prepared set of translations in the folder "Translation".

-b takes a boolean input that indicates whether to use the prepared set of results of back translations in the folder "Translation".

The default target language is English, and the prepared translation and back-translation results will are not used by default.

Sample run: python goolge_trans_method_cleaned.py -l English -t True -b True  

# evaluate_cleaned_version.py
This file contains the code to evaluate the results outputted by "goolge_trans_method_cleaned.py".

The output of this code is the Acc of LexGen and F1 Score of LexGap. 
 
This file takes 1 argument.

-l takes a string input that indicates the target language.

The default target language is English.

Sample run: python evaluate_cleaned_version.py -l English





