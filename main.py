import readFile
import ppdb
import preprocessing
import aligner
import evaluate
import tools

# fileName_PPDB = './Resources/ppdb.txt'
fileName_PPDB = './Resources/ppdb-2.0-xxl-lexical_out_stemming.txt'
fileName_PPDBex ='./Resources/ppdbex.txt'
fileName = './dataset/dataset.txt'

file_output = open("./hasil/output.txt", "w")
file_precision = open("./hasil/precision.txt", "w")
file_recall = open("./hasil/recall.txt", "w")
file_F1 = open("./hasil/F1.txt", "w")

alreadyAlign = []

recallAverage = []
precisionAverage = []
F1Average = []

# PPDB
ppdbDict = ppdb.loadPPDB(fileName_PPDB)
ppdbDictex = ppdb.loadPPDBex(fileName_PPDBex)

# Read File
sentencesAlign, goldAnnotation = readFile.dataAlign(fileName)

# Preprcessing Gold Anotation
goldAnnotation = preprocessing.deleteNull(goldAnnotation)
listAnnotation = preprocessing.cleanGoldAnno(goldAnnotation)

for i in range(len(sentencesAlign)):
    sentence1 = sentencesAlign[i][0]
    sentence2 = sentencesAlign[i][1]

    # Preprocessing
    sentenceToken1 = preprocessing.tokenize(sentence1)
    sentenceToken2 = preprocessing.tokenize(sentence2)

    sentenceLemma1 = preprocessing.stemming(sentenceToken1)
    sentenceLemma2 = preprocessing.stemming(sentenceToken2)

    # Aligner
    cekidentical = aligner.alignIdenticalWords(sentenceLemma1, sentenceLemma2)
    cekSimilar = aligner.alignWordSimilarity(sentenceLemma1, sentenceLemma2, ppdbDict)
    cekSequences = aligner.alignSequences(sentenceLemma1, sentenceLemma2)
    cekneighbor = aligner.alignTextContext(sentenceLemma1, sentenceLemma2, ppdbDict)
    cekstop = aligner.alignStop(sentenceLemma1, sentenceLemma2, ppdbDict)
    cekSimilarex = aligner.alignWordSimilarityex(sentenceLemma1, sentenceLemma2, ppdbDictex)
    # cekDep = aligner.alignDepContext(sentenceLemma1, sentenceLemma2)


    # Aligner result - Fitur yang akan dimasukkan ke hasil akhir alignment
    alreadyAlign = aligner.insertAlign(cekidentical, i, alreadyAlign)
    alreadyAlign = aligner.insertAlignPPDB(cekSimilar, i, cekidentical, alreadyAlign)
    alreadyAlign = aligner.insertAlign(cekSequences, i, alreadyAlign)
    alreadyAlign = aligner.insertAlign(cekneighbor, i, alreadyAlign)
    alreadyAlign = aligner.insertAlign(cekstop, i, alreadyAlign)
    alreadyAlign = aligner.insertAlign(cekSimilarex, i, alreadyAlign)
    # # alreadyAlign = aligner.insertAlign(cekDep, i, alreadyAlign)

    # Ubah hasil dari yang pasangan angka menjadi hasil kata dan indeks
    resultMSR = tools.transformResult(alreadyAlign[i], sentenceLemma2)

    # Memanggil fungsi dari class Evaluate untuk menampilkan hasil skor
    jumlahBenar = evaluate.jumlahBenar(resultMSR, sentenceLemma2, listAnnotation[i])
    jumlahGoldAnnotation = evaluate.jumlahGoldAnnotation(listAnnotation[i])
    jumlahDariSistem = evaluate.jumlahDariSistem(resultMSR)
    precision = evaluate.precision(jumlahBenar, jumlahDariSistem)
    recall = evaluate.recall(jumlahBenar, jumlahGoldAnnotation)
    F1 = evaluate.F1Measure(precision, recall)

    # Hitung rata-rata precision, recall dan F1
    precisionAverage.append(precision)
    recallAverage.append(recall)
    F1Average.append(F1)

    print("========================================")
    print("Sentence Lemma 1 :", sentenceLemma1)
    print("Sentence Lemma 2 :", sentenceLemma2)
    print("Gold Annotation  :", evaluate.printAnnotation(sentenceLemma2, goldAnnotation[i]))
    file_output.write("========================================" + '\n')
    file_output.write("Sentence Lemma 1 : " + str(sentenceLemma1) + '\n')
    file_output.write("Sentence Lemma 2 : " + str(sentenceLemma2) + '\n')
    file_output.write("Gold Annotation  : " + str(evaluate.printAnnotation(sentenceLemma2, goldAnnotation[i])) + '\n\n')


    print("")
    print("Identical Words :", cekidentical)
    file_output.write("Identical Words : " + str(cekidentical) + '\n')
    print("Identical from PPDB :", cekSimilar)
    file_output.write("Identical from PPDB : " + str(cekSimilar) + '\n')
    print("Identical Sequence Words :", cekSequences)
    file_output.write("Identical Sequence Words : " + str(cekSequences) + '\n')
    print("Identical Neighbor Content Words :", cekneighbor)
    file_output.write("Identical Neighbor Content Words : " + str(cekneighbor) + '\n')
    print("Identical StopWords :", cekstop)
    file_output.write("Identical StopWords : " + str(cekstop) + '\n')
    print("Identical from PPDBext :", cekSimilarex)
    file_output.write("Identical from PPDBext : " + str(cekSimilarex) + '\n\n')

    print("")
    print("kata yang di align", alreadyAlign[i])
    print("hasil transform", resultMSR)
    file_output.write("kata yang di align : " + str(alreadyAlign[i]) + '\n')
    file_output.write("hasil transform : " + str(resultMSR) + '\n\n')

    file_precision.write(str(precision) + '\n')
    file_recall.write(str(recall) + '\n')
    file_F1.write(str(F1) + '\n')

file_precision.close()
file_recall.close()
file_F1.close()

avePre = evaluate.Average(precisionAverage)
aveRec = evaluate.Average(recallAverage)
aveF1 = evaluate.Average(F1Average)
f1m = evaluate.f1measureTotal(avePre, aveRec)

print("")
print("===================:Hasil akhir:=========================")
print("Rata-rata Precision :", avePre)
print("Rata-rata Recall :", aveRec)
print("F1measure total :", aveF1)
file_output.write("===================:Hasil akhir:=========================" + '\n')
file_output.write("Rata-rata Precision : " + str(avePre) + '\n')
file_output.write("Rata-rata Recall : " + str(aveRec )+ '\n')
file_output.write("F1measure total : " + str(aveF1))
file_output.close()