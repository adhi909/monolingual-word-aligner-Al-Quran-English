import preprocessing

def precision(jumlahBenar, jumlahDariSistem):
    try:
        precision = jumlahBenar/jumlahDariSistem
    except ZeroDivisionError:
        precision = 0
    return round(precision,2)

def recall(jumlahBenar, goldAnnotation):
    recall = jumlahBenar/goldAnnotation
    return round(recall,2)


def F1Measure(precision, recall):
    if precision and recall != 0:
        F1 = 2*precision*recall/(precision+recall)
    else:
        F1=0
    return round(F1,2)

def f1measureTotal(precision, recall):
    if precision and recall != 0:
        F1 = 2*precision*recall/(precision+recall)
    else:
        F1=0
    return round(F1,4)

def jumlahBenar(alreadyAlign, sentence2, listAnnotation):
    true = 0
    # print(listAnnotation)
    # print(sentence2)
    # print(len(listAnnotation), len(sentence2))
    for i in range(len(alreadyAlign)):
        for j in range(len(sentence2)):
            # print(listAnnotation[j])
            if alreadyAlign[i][0] == sentence2[j]:
                listAnnotemp = preprocessing.toLowerCase(listAnnotation[j])
                if str(alreadyAlign[i][1]) in listAnnotemp:
                        true += 1
    return true

def jumlahGoldAnnotation(goldAnnotation):
    a = 0
    for i in range(len(goldAnnotation)):
        if not goldAnnotation[i]:
            continue
        else:
            a += len(goldAnnotation[i])
    return a

def jumlahDariSistem(alreadyAlign):
    true = len(alreadyAlign)
    return true

def Average(average):
    result = sum(average)/len(average)
    return round(result,4)

def printAnnotation(sentence2, GA):
    temp = []
    for i in range (len(sentence2)):
        temp.append([sentence2[i], GA[i]])
    return temp
