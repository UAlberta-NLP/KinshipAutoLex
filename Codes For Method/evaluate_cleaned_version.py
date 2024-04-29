#languages = ["English", "Spanish", "Russian", "French", "German", "Mandarin", "Persian", "Polish", "Arabic", "Italian", "Mongolian", "Hungarian", "Hindi"]  
#languages = [ "Hindi"]
import argparse

f_concepts = open("./Documents/concepts", "r", encoding="utf-8")
concept_matching = {}
concept_matching_rev = {}
has_concept = []
for line in f_concepts.readlines()[1:]:
    tem = line.strip().split("	")
    concept_matching[tem[1]] = tem[2]
    concept_matching_rev[tem[2]] = tem[1]
    has_concept.append(tem[1])
f_concepts.close()
# print(has_concept)

new_vertical_filter = True
column = 0

def evaluate():
    f_gloss = open("./Documents/kinship_gloss.txt", "r", encoding="utf-8")
    source_languages = {}
    lexicalizations = {}
    gloss_concept = []
    for line in f_gloss.readlines():
        line = line.strip().split("    ")

        source_word = line[0].strip()
        source_language = line[-1].strip()
        concept = line[1].strip()
        lexicalizations[concept] = []
        source_languages[concept] = source_language
        gloss_concept.append(concept)
    f_gloss.close()    
    
    seed_words_langauge_count = {}
    for concept, language in source_languages.items():
        if language in seed_words_langauge_count.keys():
            seed_words_langauge_count[language] += 1
        else:
            seed_words_langauge_count[language] = 1
    

    f_words = open("./Documents/words", "r", encoding="utf-8")

    concepts_tested = set(source_languages.keys())

    words_list  = f_words.readlines()

    f_gaps = open("./Documents/gaps", "r", encoding="utf-8")
    gaps_gold = f_gaps.readlines()
    f_gaps.close()
    
    
    
    
    
    gaps_golden_set = set()
    count_tem = 0
    for line in gaps_gold:
        if count_tem > 0:
            line = line.strip().split("	")
            concept_abbr = line[2]
            if concept_abbr[0] != "o" and concept_abbr[0] != "x":
                concept = concept_matching_rev[concept_abbr]
                language = line[1]
                if language == target_language:
                    gaps_golden_set.add(concept)
        count_tem += 1
    
    source_language_seed_word_used = set()
    for concept, language in source_languages.items():
        if language == target_language:
            source_language_seed_word_used.add(concept)

    

    for line in words_list:
        tem = line.strip().split("	")
        lang = tem[0]
        word = tem[2]
        concept = tem[4]
        # print(concept)
        if concept in concepts_tested:

            if lang == target_language:
                if len(word.split()) == 1:
                    lexicalizations[concept].append(word.strip())
                #lexicalizations[concept].append(word)
    concepts_tested = concepts_tested - source_language_seed_word_used

    f_words.close()

    # print(lexicalizations)
    
    f_result = open("./Results/result-%s.txt"%target_language, mode="r", encoding="utf-8")
    
    # 
    types = {"Lex/Gap":0,
             "Lex/Lex":0,
             "Lex/Lex1":0,
             "Gap/Lex":0,
             "Gap/Gap":0,
             "None/Gap":0,
             "None/Lex":0}
    
    for line in f_result.readlines():
        line = line.split("        ")
        concept = line[0].strip()
        word = line[1].strip()
        prediction = line[3].strip()
        
        source_language = line[2].strip()
        
        if column == 1:
            print(concept)
            
        if column == 2:
            if len(lexicalizations[concept]) > 0:
                print("Has lexicalization")
            elif concept in gaps_golden_set: 
                print("In Gap file")
            else:
                print("No information")
        if column == 3:
            if len(lexicalizations[concept]) == 0:
                print("No lexicalization provided")
            else:
                print(lexicalizations[concept])
            
        if prediction == "True":
            if column == 6:
                print("gap")
            if len(lexicalizations[concept]) == 0:
                if concept in gaps_golden_set:
                    types["Gap/Gap"] += 1
                    # print("correct")
                    if column == 7 or column == 8:
                        print("correct")
                else:
                    types["None/Gap"] += 1
                    # print("correct")
                    if column == 7 or column == 8:
                        print("correct")
            else:
                types["Lex/Gap"] += 1
                if column == 7 or column == 8:
                        print("not correct")
        
        if column == 4:
            print(word)
        
        if column == 5:
            print(line[4].strip())
        
        if prediction == "False":
            if column == 6:
                print("not gap")
                
            if len(lexicalizations[concept]) > 0:
                if word in lexicalizations[concept]:
                    types["Lex/Lex"] += 1
                    if column == 7 or column == 8:
                        print("correct")
                else:
                    types["Lex/Lex1"] += 1
                    # print("here")
                    
                    if column == 7:
                        print("correct")
                    if column == 8:
                        print("not correct")
            else:
                if concept in gaps_golden_set:
                    types["Gap/Lex"] += 1
                    # print("not correct")
                    if column == 7 or column == 8:
                        print("not correct")
                else:
                    types["None/Lex"] += 1
                    # print("not correct")
                    if column == 7 or column == 8:
                        print("not correct")

    # print(target_language) 
    # print(types["Gap/Gap"])
    # print(types["Gap/Lex"])
    # print(types["Lex/Lex"])
    # print(types["Lex/Lex1"])
    # print(types["Lex/Gap"])
    # print(types["None/Lex"])
    # print(types["None/Gap"])   
    f_result.close()
    return types

def calculate_LexGap_F1(types):
    precision = (types["Gap/Gap"])/(types["Gap/Gap"] + types["Lex/Gap"])
    recall =  (types["Gap/Gap"])/(types["Gap/Gap"] + types["Gap/Lex"])
    return precision*recall*2/(precision+recall)
def calculate_LexGen_acc(types):
    total_number = 0
    for value in types.values():
        total_number += value
    correct_prediction_number = types["Gap/Gap"] + types["Lex/Lex"] + types["None/Gap"]
    
    return correct_prediction_number/total_number

def main():
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-l', '--target_language', type=str, required=False, default="English", help="The target language for this run")
    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print(f"target language: {args.target_language}")
    
    
    global target_language
    target_language = args.target_language
    
    types = evaluate()    
    print("LexGap F1 Score: ", round(calculate_LexGap_F1(types),3))
    print("LexGen Accuracy: ", round(calculate_LexGen_acc(types),3))
if __name__ == '__main__':
    main()

 