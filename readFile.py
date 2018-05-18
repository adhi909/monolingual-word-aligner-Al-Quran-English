import os
import re

def dataAlign(filename):
    fo = open(os.path.join(filename), "r")

    sentencesAlign = []
    goldAnnotation = []
    for line in fo.readlines():
        if line.split() == [] :
            continue
        if line.split()[0] != "NULL" :
            LoLi = line.rstrip('\n')
        if line.split()[0] == "NULL" :
            LoL = [LoLi, re.sub('\s*(?:\([^/]*/\s*/\s*\)|NULL)\s*',' ', line)]
            sentencesAlign.append(LoL)

            goldAnno = re.findall('\s*(\([^/]*/\s*/\s*\))\s*',line)
            goldAnnotation.append(goldAnno)

    return sentencesAlign, goldAnnotation