from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

fileName = "./Resources/ppdb-2.0-xxl-lexical.txt"
fileName_out = "./Resources/ppdb-2.0-xxl-lexical_out.txt"

ppdbFile = open(fileName, 'r', encoding="utf8")
ppdbFile_out = open(fileName_out, 'w', encoding="utf8")

for line in ppdbFile:
    line = line.split(" ||| ")
    ppdbFile_out.write(line[1] + "	" + line[2] + "\n")