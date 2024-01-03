import json
 
# Opening JSON file
f = open('ontology.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)

for i in range(len(data)):
    print(data[i]["child_ids"])




# Closing file
f.close()