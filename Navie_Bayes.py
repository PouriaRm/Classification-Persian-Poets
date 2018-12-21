
from using_nlp import getAuthors,countWordsInClass


def Probability(self, doc, dclass=""):
    """Calculates the probability for a class dclass given a document doc"""
    if dclass:
        sum_dclass = self.sum_words_in_class(dclass)
        prob = 0

        # d = Document(self.__vocabulary)
        # d.read_document(doc)

        for j in len(getAuthors()):
            sum_j = self.sum_words_in_class(j)
            prod = 1
            for i in d.Words():
                wf_dclass = 1 + self.__document_classes[dclass].WordFreq(i)
                wf = 1 + self.__document_classes[j].WordFreq(i)
                r = wf * sum_dclass / (wf_dclass * sum_j)
                prod *= r
            prob += prod * self.__document_classes[j].NumberOfDocuments() / self.__document_classes[
                dclass].NumberOfDocuments()
        if prob != 0:
            return 1 / prob
        else:
            return -1
    else:
        prob_list = []
        for dclass in self.__document_classes:
            prob = self.Probability(doc, dclass)
            prob_list.append([dclass, prob])
        prob_list.sort(key=lambda x: x[1], reverse=True)
        return prob_list

#print(countWordsInClass(2))