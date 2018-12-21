from __future__ import unicode_literals

import math
from hazm import *
import os, fnmatch

from nltk import FreqDist
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('mysql+pymysql://root:root@localhost:3306/nlp?charset=utf8')
metadata = MetaData(db)
Base = declarative_base()
session = sessionmaker()
session.configure(bind=db)
s = session()


class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, )
    author = Column(Integer, nullable=False)
    century = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, )
    century = Column(Integer, nullable=False)
    century_name = Column(Integer, nullable=False)
    docs = Column(Integer, nullable=False)



def getAuthors():
    authorList = s.query(Author).all()
    return authorList

def getWordCount(word,id):
    token = s.query(Token).filter(Token.name == word).filter(Token.author == str(id)).first()
    counter=0
    if token:
        counter=token.count

    # print(counter)
    return counter

def getNumberofDocs(id):
    author = s.query(Author).filter(Author.id == id).first()
    return author.docs

# make boolean type if learn so push it in database but if it's test don't push it in dbase.
def tokenising():
    normalize = Normalizer()
    authors = getAuthors()
    listoffiles = os.listdir("data/data/")
    for author in authors:
        counter = 0
        # pattern = "jami-Ninth-*.txt"
        pattern = author.name + "-" + author.century_name + "-*.txt"
        for entry in listoffiles:
            if counter <= 3:
                if fnmatch.fnmatch(entry, pattern):
                    file = open("data/data/" + entry, "rb")
                    counter = counter + 1

                    raw_data = file.read().decode("UTF-8")
                    file.close()
                    normalData = normalize.normalize(raw_data)
                    tokenizeData = word_tokenize(normalData)

                    got = [item.replace("\u200c", "") for item in tokenizeData]
                    # print(got)
                    for word in got:
                        token = s.query(Token).filter(Token.name == word).filter(Token.author == author.id).first()
                        if not token:
                            token = Token(name=word, count=1, author=author.id, century=author.century)
                            s.add(token)
                            s.commit()
                        else:

                            token.count += 1
                            s.commit()
            else:
                break

def countWordsInClass(authorId):

    # print(authorId)
    tokens=s.query(Token).filter(Token.author==authorId).all()
    counter=0
    for a in tokens:
        counter+=a.count
    return counter

def test_file_reader():
    authors = getAuthors()
    listoffiles = os.listdir("test/")

    #for entry in listoffiles:
        #for author in authors:
            #pattern = author.name + "-" + author.century_name + "-*.txt"
            #if fnmatch.fnmatch(entry, pattern):
    entry = "frdvsi-Fourth-10091.txt"
    res = Probability(entry)
    print("frdvsi" + ": " + entry+ ": " + str(res))


def read_document_test(entry):
    normalize = Normalizer()


    file = open("test/" + entry, "rb")
    raw_data = file.read().decode("UTF-8")
    file.close()
    normalData = normalize.normalize(raw_data)
    tokenizeData = word_tokenize(normalData)

    got = [item.replace("\u200c", "") for item in tokenizeData]
    print(got)

    return got

def Probability(doc, author=""):
    """Calculates the probability for a class author given a document doc"""

    authors = getAuthors()
    if author:
        sum_author_class= countWordsInClass(author)
        prob = 0

        # d = Document(self.__vocabulary)
        # d.read_document(doc)
        d =read_document_test(doc)

        for j in authors:
            print("for author :"+j.name+".................................................")

            sum_j = countWordsInClass(j.id)
            prod = 1
            for i in d:

                wf_dclass = 1 + getWordCount(i,j.id)
                wf = 1 + countWordsInClass(j.id)
                r = wf * sum_author_class / (wf_dclass * sum_j)
                r = math.log(r, 10)
                prod *= r
                # print("author: " + str(author), "j: " + str(j.id))
                # print("prod: " + str(prod))
            prob += prod * getNumberofDocs(j.id) / getNumberofDocs(author)
            print("prob for " + j.name + "is : " + str(prob))
        if prob != 0:

            return 1 / prob
        else:
            return -1
    else:
        prob_list = []
        #author is like getAuthor()
        for author in authors:
            prob = Probability(doc, author.id)
            prob_list.append([author.name, prob])
        prob_list.sort(key=lambda x: x[1], reverse=True)
        return prob_list


#test_file_reader()
        #authors=getAuthors()
#for j in authors:
 #   print(j.id)

#print(countWordsInClass(1))


