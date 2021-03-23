import os
import pickle

path = os.getcwd()
db = pickle.load(open(os.path.abspath(os.path.join(path, os.pardir))\
                            +'/sMDT/database.p', 'rb'))

labels = []

# Get all the labels in the database
for tube,tubeData in db.items():
    for item in tubeData.keys():
        if item not in labels:
            labels.append(item)
print(labels)

f = open("database.csv",'w')
f.write("Code,")
for item in labels:
    f.write(item + ',')
f.write("\n")

for tube,tubeData in sorted(db.items(), reverse=True):
    f.write(tube + ',')
    for item in labels:
        if item in tubeData:
            if item == '': f.write('No Data')
            if isinstance(tubeData[item],list):
                for data in tubeData[item]:
                    data = str(data).replace(',',' ').replace('\n','')
                    f.write(str(data)+'|')
            else:
                f.write(str(tubeData[item]))
        else:
            f.write('No Data')
        f.write(',')
    f.write('\n')
