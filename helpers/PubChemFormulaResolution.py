import requests
url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/HAuCl4/synonyms/json'
response = requests.get(url)
my_resp = response.json()
for id, info in my_resp.items():
    print(id)
    for key in info:
        print(key + '-', info[key])

synonym_list = my_resp['InformationList']['Information']
#print(synonym_list)
#print(synonym_list.pop())
print([s["Synonym"][0] for s in synonym_list])