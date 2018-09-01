import csv

with open('concepts_old.csv') as fr:
  reader = csv.reader(fr)
  token_list = list(reader)
fr.close()

fw = open('temp.txt', 'w')
for word in token_list:
    data = word[0].split()
    for temp in data:
        b = False
        count = 0
        if not temp.isupper():
            chList = list(temp)
            for ch in chList:
                # Ignore first character
                if count != 0:
                    if not ch.isupper():
                        b = b or False
                    else:
                        b = b or True
                count += 1

        if b:
            print(temp)
            fw.write(temp)
            fw.writelines("\n")    
fw.close()