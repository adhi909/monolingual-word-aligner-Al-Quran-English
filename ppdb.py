ppdbSim = 0.9


def loadPPDB(fileName_PPDB):
    ppdbFile = open(fileName_PPDB, 'r', encoding="utf8")

    ppdbDict = {}
    for line in ppdbFile:
        if line == '\n':
            continue
        tokens = line.split("	")
        tokens[1] = tokens[1].strip()
        ppdbDict[(tokens[0], tokens[1])] = ppdbSim

    return ppdbDict

def presentInPPDB(word1, word2, ppdbDict):
    if (word1.lower(), word2.lower()) in ppdbDict:
        return True
    elif (word2.lower(), word1.lower()) in ppdbDict:
        return True

def wordSim(word1, word2, ppdbDict):
    if presentInPPDB(word1, word2, ppdbDict):
        return ppdbSim
    else:
        return 0

def loadPPDBex(fileName_PPDBex):
    ppdbFile = open(fileName_PPDBex, 'r', encoding="utf8")

    ppdbDictex = {}
    for line in ppdbFile:
        if line == '\n':
            continue
        tokens = line.split('\t')
        tokens[1] = tokens[1].strip()
        ppdbDictex[(tokens[0], tokens[1])] = ppdbSim

    return ppdbDictex


def presentInPPDBex(word1, word2, ppdbDictex):
    if (word1.lower(), word2.lower()) in ppdbDictex:
        return True
    if (word2.lower(), word1.lower()) in ppdbDictex:
        return True