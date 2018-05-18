from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

punctuations = ['(','-lrb-',".",',','-','?','!',';','_',':','{','}','[','/',']','...','"','\'',')', '-rrb-',"'s",'"','ha',"'",'wa']
stopwords = stopwords.words('english')
stemmer = PorterStemmer()

def tokenize(sentences):
    return sentences.split()

def stemming(sentences):
    result = []

    for i in range(len(sentences)):
        result.append(stemmer.stem(sentences[i]))
    return result

def cleanGoldAnno(goldAnnotation):
    result= []
    for i in range(len(goldAnnotation)):
        goldAnno = []
        for j in range(len(goldAnnotation[i])):
            cek = re.findall('[^p][0-9][0-9]|[^p0-9][0-9]',goldAnnotation[i][j].replace("p", "")) #dengan P dihitung->[0-9][0-9]|[0-9] #[0-9][0-9]|[0-9]|p[0-9][0-9]|p[0-9] #tanpa P -> [^p][0-9][0-9]|[^p0-9][0-9]
            for k in range (len(cek)):
                cek[k] = cek[k].replace("(","").strip()
            goldAnno.append(cek)
        result.append(goldAnno)

    return result

def cleanP(listAnno):
    cek = ""
    result = []
    for i in range(len(listAnno)):
        for j in range(len(listAnno[i])):
            for k in range(len(listAnno[i][j])):
                cek = listAnno[i][j][k]
            listAnno[i].append(cek)
        result.append(listAnno)

    return result

def toLowerCase(sentence):
    result = [w.lower() for w in sentence]
    return result

def deleteNull(goldAnnotation):
    for i in range(len(goldAnnotation)):
        del goldAnnotation[i][0]

    return goldAnnotation