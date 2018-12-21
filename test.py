from NaiveBayes import  Pool
import os
dClass = list()
cenClass = list()
#DClasses = ["clinton",  "lawyer",  "math",  "medical",  "music",  "sex"]
from using_nlp import getAuthors
authors = getAuthors()
for author in authors:
    print(author.name)
    dClass.append(author.name)
    cenClass.append(author.century_name)
# read a learn data from pool class that we do it in our mysql table.
base = "data/data/"
p = Pool()
for i in range(len(dClass)):
    p.learn(base, dClass[i],cenClass[i])
print("finish..........................................................")


base = "test/"


dir = os.listdir(base)
for file in dir:
    res = p.Probability(base + "/" + file)
    print(": " + file + ": " + str(res))
