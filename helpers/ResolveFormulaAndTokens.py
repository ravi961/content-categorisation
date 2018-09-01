import csv
from collections import defaultdict

# Read Formula/Abbrevation/Synonym file
list1 = []
list2 = []
with open('formula.csv') as fr:
    reader = csv.reader(fr)
    formula_list = list(reader)
    for word in formula_list:
        if word[1] != "":
            list1.append(word[0])
            list2.append(word[1])
fr.close()
print(list1)
print(list2)

# Create Dictionary of Key and multiple values
d = defaultdict(list)
for i,key in enumerate(list1):
        if list2[i] not in d[key]:            #to add only unique values (ex: 'ZrO2':'ZIRCONIUM OXIDE')
            d[key].append(list2[i])
print(d)        

# Resolve Tokens
token_list = []
with open('concepts.csv') as fr:
    reader = csv.reader(fr)
    token_list = list(reader)
fr.close()

concept_list = []
for word in token_list:
    concept_list.append(word[0])

# #concept_list = ['ZrO2 Layer', 'ZrO2 Film', 'ZrO2 Nanoparticle']
formula_resolved_tokens = []

# Generate Alternate tokens
for word in concept_list:
    token = word.split()
    for temp in token:
        if d.get(temp) is not None:
            for alt in d.get(temp):
                formula_resolved_tokens.append(word.replace(temp,alt))
        
#print(concept_list)
#print(formula_resolved_tokens)
len(formula_resolved_tokens)