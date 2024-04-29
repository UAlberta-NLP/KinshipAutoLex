children = { "Sb": ["Br", "Ss"], "Pr": ["Fa", "Mo"], "Ch":["So", "Da"], "Pa": ["Fa", "Mo"],  }

subdomains = ["siblings", "nibling", "cousins", "auncle", "grandchildren", "grandparents"]
abbrs = ["Sb", "Sb;Ch", "Pa;Sb;Ch", "Pa;Sb", "Gr;Ch", "Gr;Pr"]

f_new_concepts = open("new_concepts", "w")
f_new_relations = open("new_relations", "w")
for i in range(len(subdomains)):
    concepts = set()
    subdomain = subdomains[i]
    queue = [abbrs[i]]

    if subdomain == "grandparents":
        children["Gr"] = ["Fa", "Mo"]
    elif subdomain == "grandchildren":
        children["Gr"] = ["So", "Da"]

    expanded_nodes = set()
    triples = []
    def expanding(node):
        parts = node.split(";")
        expanded = []
        for i in range(len(parts)):
            
            tem = parts[i]
            
            if tem in children.keys():
                two_children = children[tem]
                
                triple = [node]
                
                
                for c in two_children:
                    parts[i] = c
                    new_node = ";".join(parts)
                    triple.append(new_node)
                    if new_node not in expanded_nodes:
                        expanded.append(new_node)
                        expanded_nodes.add(new_node)
                        # print("here")
                
                if tem == "Sb":
                    triple.append("male sibling/female sibling")
                if tem == "Ch":
                    triple.append("male child/female child")
                if tem == "Pr" or tem == "Pa":
                    triple.append("male parent/female parent")
                if tem == "Gr":
                    if subdomain == "grandparents":
                        triple.append("male parent/female parent")
                    else:
                        triple.append("male child/female child")
                triples.append(triple)
                
            
                parts[i] = tem
                
        if "El" not in parts and "Yn" not in parts:
            # print(parts)
            triple = [node]
            
            if subdomain == "auncle":
                parts.insert(1,"El")
                if ";".join(parts) not in expanded_nodes:
                    expanded.append(";".join(parts))
                    expanded_nodes.add(";".join(parts))
                triple.append(";".join(parts))
                parts[1] = "Yn"
                if ";".join(parts) not in expanded_nodes:
                    expanded.append(";".join(parts))
                    expanded_nodes.add(";".join(parts))
                triple.append(";".join(parts))
            elif subdomain in ["cousins", "siblings", "nibling"]:
                parts.insert(0,"El")
                
                # print(";".join(parts))
                # print("here")
                if ";".join(parts) not in expanded_nodes:
                    expanded.append(";".join(parts))
                    expanded_nodes.add(";".join(parts))
                triple.append(";".join(parts))
                
                
                parts[0] = "Yn"
                
                if ";".join(parts) not in expanded_nodes:
                    expanded.append(";".join(parts))
                    expanded_nodes.add(";".join(parts))
                triple.append(";".join(parts))
            if subdomain == "siblings" or subdomain == "auncle" or subdomain == "nibling":
                triple.append("elder sibling/younger sibling")
                triples.append(triple)
            if subdomain == "cousins":
                triple.append("elder child/younger child")
                triples.append(triple)
        return expanded    
            



    mapping = {"El":"elder", "Yn":"younger","Sb":"sibling","Pr": "parent", "Pa":"parent", "Br": "male sibling", "Ss": "female sibling", "Ch":"child", "So":"male child", "Da":"female child", "Fa":"male parent", "Mo":"female parent"}
    if subdomain == "grandparents":
        mapping["Gr"] = "parent"
    elif subdomain == "grandchildren":
        mapping["Gr"] = "child"


    def print_name(abbr):
        parts = abbr.split(";")
        text = ""
        recording = False
        storing = False
        for i in range(len(parts)):
            if i == 0:
                if parts[0] == "El" or parts[0] == "Yn":
                    if subdomain == "nibling":
                        storing = mapping[parts[0]]
                    else:
                        recording = mapping[parts[0]]
                else:
                    text = text + mapping[parts[0]]
            elif i == len(parts) -1:
                
                text = mapping[parts[i]] + " of " + text
                if recording:
                    text = recording + " "  + text
                if storing:
                    text = storing + " " + text
                    storing = False
                
            else:
                
                if parts[i] == "El" or parts[i] == "Yn":
                    storing = mapping[parts[i]] 
                else:
                    if subdomain == "nibling":
                        if storing:
                            text = storing + " " + mapping[parts[i]] + text
                            storing = False
                        else:
                            text = mapping[parts[i]] + " of " + text
                    else:
                        if storing:
                            text = storing + " " + mapping[parts[i]] + " of " + text
                            storing = False
                        else:
                            text = mapping[parts[i]] + " of " + text
        if text[-2] == "f" and text[-3] == "o":    
            text = text[:-3].strip()
        return text

    while len(queue) != 0:
        node_now = queue.pop(0)
        new_nodes = expanding(node_now)
        queue = queue + new_nodes


    for triple in triples: 
        concepts.add(triple[0]) 
        concepts.add(triple[1])
        concepts.add(triple[2])
        f_new_relations.write(subdomain + "	" + triple[1]   + "	"+ triple[0]  +"\n" )
        f_new_relations.write(subdomain + "	" + triple[2]   + "	"+ triple[0]  +"\n" )
        
        
    for c in concepts:
        f_new_concepts.write(subdomain + "	" + print_name(c)    +"	"+ c + "	" +"\n" )