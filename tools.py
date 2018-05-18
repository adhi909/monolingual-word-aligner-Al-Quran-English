import os
import preprocessing
from nltk.parse.stanford import StanfordDependencyParser

os.environ['CLASSPATH'] = "./resources/"

#untuk identifikasi urutan kata
def cekSeq(tempAcr,p,name):
    uh = []
    for i in range(len(tempAcr)):
        if name[0] == tempAcr[i][0][0]:
            temo = tempAcr[i][1]
            if p == 1:
                p = 2
            for m in range(p):
                for gr in range(len(tempAcr)):
                    if temo + m == tempAcr[gr][1]:
                        uh.append(tempAcr[gr])
                        uh.append(tempAcr[i])
    return uh

#untuk menemukan posisi indeks kata
def findPos(sentence1,kata1,kata2):
    pos = []
    for h in range(len(sentence1)):
        if h <= len(sentence1)-1:
            if sentence1[h] == kata1 and sentence1[h+1] == kata2:
                pos.append([h,h+1])
    return pos

#untuk mengubah hasil akhir alignment
def transformResult(alreadyalign,sentence2):
    result = []
    for mi in range(len(alreadyalign)):
        result.append([sentence2[alreadyalign[mi][0]-1],alreadyalign[mi][1]])
    s = []
    for i in result:
       if i not in s:
          s.append(i)
    return s

#untuk menghapus stop words
def deleteStop(alreadyAlign,sentence):
    temp = []
    fix = []
    for n in range(len(alreadyAlign)):
        if sentence[alreadyAlign[n][0]-1].lower() in preprocessing.stopwords + preprocessing.punctuations:
            temp.append(alreadyAlign[n])
    for m in range(len(alreadyAlign)):
        if alreadyAlign[m] not in temp:
            fix.append(alreadyAlign[m])
    return fix

# untuk identifikasi parser
def depParser(sentence):
    word = ''.join(sentence)

    english_parser = StanfordDependencyParser('./resources/stanford-parser-3.4.1-models.jar')
    result = [list(parse.triples()) for parse in english_parser.raw_parse_sents(word)]

    return result