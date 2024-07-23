from googletrans import Translator
from copy import deepcopy
import csv
import sys
import argparse

translator = Translator()


f_words = open("./Documents/words", "r", encoding="utf-8")
f_concepts = open("./Documents/concepts", "r", encoding="utf-8")
f_relations = open("./Documents/relations", "r", encoding="utf-8")
f_google_trans_lang = open("./Documents/google_trans_language.txt", "r", encoding="utf-8")
f_gaps = open("./Documents/gaps", "r", encoding="utf-8")
f_gloss = open("./Documents/kinship_gloss.txt", "r", encoding="utf-8")




concept_matching = {}
concept_matching_rev = {}
word_has = {}

for line in f_concepts.readlines()[1:]:
    tem = line.strip().split("	")
    concept_matching[tem[1]] = tem[2]
    concept_matching_rev[tem[2]] = tem[1]
    word_has[tem[1]] = []

google_lang_abbr_match = {}
google_lang_abbr_match_rev = {}

for line in f_google_trans_lang.readlines():
    line = line.split()
    abbr = line[0].split("=")[1] 
    language = line[1]
    google_lang_abbr_match[language] = abbr
    google_lang_abbr_match_rev[abbr] = language

parents_matching = {}
children_matching = {}
for line in f_relations.readlines()[1:]:
    tem = line.strip().split("	")

    if(tem[1] in parents_matching.keys()):
        parents_matching[tem[1]].append(tem[2])
    else:
        parents_matching[tem[1]] = [tem[2]]

    if(tem[2] in children_matching.keys()):
        children_matching[tem[2]].append(tem[1])
    else:
        children_matching[tem[2]] = [tem[1]]
    
opposite = {}
opposite["Br"] = "Ss"
opposite["Ss"] = "Br"
opposite["Da"] = "So"
opposite["So"] = "Da"
opposite["Fa"] = "Mo"
opposite["Mo"] = "Fa"
opposite["Yn"] = "El"
opposite["El"] = "Yn"

no_opp = ['Pa','Sb','Gr',"Ch","Pr"]    

def node_depth(concept, depth=0):
    parent_node = parents_matching[concept][0]
    if(parent_node == "#"):
        return depth
    else:
        return node_depth(parent_node, depth+1)

def find_root(concept):
    concept_abbr = concept_matching[concept]
    parent_node = parents_matching[concept_abbr][0]
    if(parent_node == "#"):
        return concept
    else:
        return find_root(concept_matching_rev[parent_node])



all_concepts = set(concept_matching_rev.keys())

words_list  = f_words.readlines()
f_words.close()

    


concepts_filters_filter_out = {}
concepts_covered_word_matching = {}
words_gloss = {}
for line in f_gloss.readlines():
    line = line.strip().split("    ")
    words_gloss[line[0]] = line[2].strip()
    source_word = line[0].strip()
    source_language = line[-1].strip()
    concept = line[1].strip()
    concepts_filters_filter_out[concept] = "not filtered out"
    # print(concept, source_word, source_language)
    concepts_covered_word_matching[concept] = (source_word, source_language)
f_gloss.close()


concept_translation_match = {}
gaps = []

def get_translations():
    if not use_prepared_translation:
        for key, value in concepts_covered_word_matching.items():
            source_language = value[1]
            source_language_abbr = google_lang_abbr_match[value[1]]
            source_language_word = value[0] 
            query_language = "%s: %s"%(value[0], words_gloss[value[0]])

            result = translator.translate(query_language, src=source_language_abbr, dest=target_language_abbr)
        

            
            query_translation = result.text.lower()
            
            end_index = query_translation.split(":")
            if(len(end_index) == 1):
                end_index = end_index[0].split("：")
            target_word_trans = end_index[0].strip().lower()
            

            key_abbr = concept_matching[key]
            key_depth = node_depth(key_abbr)
            concept_translation_match[key] = [target_word_trans, query_translation, query_language, key_depth, source_language_word, source_language]
            #information  = {"Concept":key,  'Source language':source_language, 'Target Language': target_language, "Source Word":source_language_word, "Target Word": target_word_trans, "Query": query_language, "Query translation":query_translation}
            # writer.writerow(information)
    else:
        with open('Translation/%s_Translation.csv'%target_language, newline='',encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                key = row["Concept"]
                source_language = row["Source language"]
                source_language_word = row["Source Word"]
                target_word_trans = row["Target Word"]
                query_language = row["Query"]
                query_translation = row["Query translation"]
                key_abbr = concept_matching[key]
                key_depth = node_depth(key_abbr)
                concept_translation_match[key] = [target_word_trans, query_translation, query_language, key_depth, source_language_word, source_language]
                
def multi_word_expression_filter():
    for key in concept_translation_match.keys():
        if len(concept_translation_match[key][0].split()) > 1  or "/" in concept_translation_match[key][0] or "的" in concept_translation_match[key][0] or "或" in concept_translation_match[key][0]:
            # print(key, "      ", concept_translation_match[key][0] )
            concepts_filters_filter_out[key] = "filter 1: multi word filter"
            gaps.append(key)



def extract_neighbbors(concept_input):
    neighbor_list = []
    parents = set(parents_matching[concept_matching[concept_input]])
    for pa in parents:
        if "#" == pa:
            neighbor_list +=  ["Pa;Sb;Ch", "Gr;Pr", "Gr;Ch", "Sb;Ch", "Sb", "Pa;Sb"]
            for i in range(len(neighbor_list)):
                neighbor_list[i] = concept_matching_rev[neighbor_list[i]]
            neighbors = set(neighbor_list)
            return neighbors - set([concept_input])
    child_abbr = concept_matching[concept_input]
    child_split = child_abbr.split(";")
    for i in range(len(child_split)):
        if child_split[i] not in no_opp:
            tem = child_split[i] 
            child_split[i] = opposite[child_split[i]]
            opposite_child_abbr = ";".join(child_split)
            if opposite_child_abbr in concept_matching_rev.keys():
                opposite_child = concept_matching_rev[opposite_child_abbr]
                if opposite_child in concept_translation_match.keys():
                    neighbor_list.append(opposite_child)
            child_split[i] = tem
    neighbors = set(neighbor_list)
    return neighbors

def horizontal_filter():
    for key1, value1 in concept_translation_match.items():
        depth1 = value1[3]
        word_translation = value1[0]
        if(key1 not in gaps):
            child_abbr = concept_matching[key1]
            child_split = child_abbr.split(";")
            for i in range(len(child_split)):
                if child_split[i] not in no_opp:
                    tem = child_split[i] 
                    child_split[i] = opposite[child_split[i]]
                    opposite_child_abbr = ";".join(child_split)
                    if opposite_child_abbr in concept_matching_rev.keys():
                        opposite_child = concept_matching_rev[opposite_child_abbr]
                        if opposite_child in concept_translation_match.keys():
                            o_word = concept_translation_match[opposite_child][0]
                            if word_translation == o_word:
                                gaps.append(key1)
                                concepts_filters_filter_out[key1] = "filter 2: horizontal filter"
                                break
                    child_split[i] = tem

def lowest_depth_and_concept(concept_set):
    concept_list = list(concept_set)
    lowest_concept = concept_list[0]
    lowest_depth = concept_translation_match[lowest_concept][3]
    for i in range(1,len(concept_list)):
        concept = concept_list[i]
        depth = concept_translation_match[concept][3]
        if depth > lowest_depth:
            lowest_depth = depth
            lowest_concept = concept
    return lowest_depth, lowest_concept



def find_all_hypernyms(concept):
    hypernym_list = set([])
    parent = set(parents_matching[concept_matching[concept]])
    hypernym_list = hypernym_list.union(parent)
    if('#' not in parent):
        for p in parent:
            p = concept_matching_rev[p]
            hypernym_list = hypernym_list.union(find_all_hypernyms(p))
    return hypernym_list

# step 3
def back_translation_filter():
    detected_not_gap = set(concept_translation_match.keys()) - set(gaps)
    if not use_prepared_back_translation_result:
        for potential in set(detected_not_gap):
            source_language = concept_translation_match[potential][5]
            query_translation = concept_translation_match[potential][1]
            seed_word = concept_translation_match[potential][4]
            source_language_abbr = google_lang_abbr_match[source_language]
            
            back_translation_query = translator.translate(query_translation, src=target_language_abbr, dest=source_language_abbr).text

            end_index1 = back_translation_query.split(":")
            if(len(end_index1) == 1):
                end_index1 = end_index1[0].split("：")
                if(len(end_index1) == 1):
                    end_index1 = end_index1[0].split(",")
                    if(len(end_index1) == 1):
                        end_index1 = end_index1[0].split("，")

            word_translation1 = end_index1[0].strip().lower()

            #print(seed_word, "   " ,word_translation1, "    ", back_translation_query)
            
            if word_translation1 != seed_word :
                gaps.append(potential)
                concepts_filters_filter_out[potential] = "filter 3: back translation filter"
    else:
        with open('Translation/%s_Back_Translation_result.csv'%target_language, newline='',encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                potential = row["Concept"]
                back_translation_result = row["Result"]
                if potential in detected_not_gap:
                    if back_translation_result != "Success":
                        gaps.append(potential)
                        concepts_filters_filter_out[potential] = "filter 3: back translation filter"
def vertical_filter():
    gaps_copy = deepcopy(gaps)
    for concept in (set(concept_translation_match.keys()) - set(gaps_copy)):
        parent = parents_matching[concept_matching[concept]]
        neighbors = extract_neighbbors(concept)
        lexicalization = concept_translation_match[concept][0].strip()
        if "#" not in parent:
            for neighbor in neighbors:
                neighbor_abbr = concept_matching[neighbor]
                neighbor_parent = set(parents_matching[neighbor_abbr])
                if len(set(parent).intersection(neighbor_parent) )  > 0:
                    parent_share = list(set(parent).intersection(neighbor_parent))[0]
                    if concept_matching_rev[parent_share] not in gaps_copy:
                        if concept_matching_rev[parent_share] in concept_translation_match.keys():
                            parent_lexicalization = concept_translation_match[concept_matching_rev[parent_share]][0].strip()
                            if parent_lexicalization == lexicalization:
                                if neighbor not in gaps_copy:
                                    gaps.append(concept_matching_rev[parent_share])
                                    concepts_filters_filter_out[concept_matching_rev[parent_share]] = "filter 4: new vertical filter"
                                else:
                                    concepts_filters_filter_out[concept] = "filter 4: new vertical filter"
                                    gaps.append(concept)


# English Russian Spanish French German Mandarin Persian Polish Arabic Hindi Hungarian Italian Mongolian

def main():
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-l', '--target_language', type=str, required=False, default="English", help="The target language for this run")
    parser.add_argument('-t', '--use_prepared_translation', type=bool, required=False, default=False, help="Use prepared translation or not")
    parser.add_argument('-b', '--use_prepared_back_translation_result', type=bool, required=False, default=False, help="Use prepared back translation result or not")
    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print(f"target language: {args.target_language}")
    
    
    global target_language
    target_language = args.target_language
    
    
    global target_language_abbr
    target_language_abbr = google_lang_abbr_match[target_language]
    
    global use_prepared_translation
    use_prepared_translation = args.use_prepared_translation
    
    global use_prepared_back_translation_result
    use_prepared_back_translation_result = args.use_prepared_back_translation_result
    
    get_translations()
    multi_word_expression_filter()
    horizontal_filter()
    back_translation_filter()
    vertical_filter()     

if __name__ == '__main__':
    main()
                    
    f_output = open("./Results/result-%s.txt"%target_language, mode="w", encoding="utf-8")

    for key, value in concept_translation_match.items():
        print(key, "\t", value[0], "\t", key in gaps, "\t", concepts_filters_filter_out[key])
        f_output.write(key + "        " + value[0] + "        " + value[5] + "        " + str(key in gaps) + "        " + concepts_filters_filter_out[key] +  "\n" )


