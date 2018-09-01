import csv

with open('concepts_new.csv') as fr:
  reader = csv.reader(fr)
  token_list = list(reader)
fr.close()

fw = open('temp.csv', 'w')
for word in token_list:
    data = word[0].split()
    for temp in data:
        b = False
        count = 0
        if temp.isupper() and len(temp) > 1:
            print(temp)
            fw.write(temp)
            fw.writelines("\n")  
fw.close()