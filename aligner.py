import preprocessing
import ppdb
import tools

alreadyAlign = []

#alignment untuk identical words
def alignIdenticalWords(sentence1, sentence2):
    identicalWords = []
    t = 1
    for i in range(len(sentence1)):
        for j in range(len(sentence2)):
            if sentence1[i].lower() and sentence2[j].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                if sentence1[i].lower() == sentence2[j].lower() and sentence2[j] not in preprocessing.stopwords + preprocessing.punctuations :
                    identicalWords.append([j+1,t])

        t = t + 1

    #align titik di akhir kalimat
    identicalWords.append([len(sentence2),len(sentence1)])
    return identicalWords

def insertAlign(alignResult, i, alreadyAlign):
    alreadyAlign.append([])

    for k in range(len(alignResult)):
        if alignResult[k] not in alreadyAlign[i] :
            temp = [alignResult[k]]
            alreadyAlign[i].extend(temp)
    return alreadyAlign

# alignment berdasarkan PPDB
def alignWordSimilarity(sentence1, sentence2, ppdbDict):
        wordsSimilarity = []
        t = 1
        for i in range(len(sentence1)):
            for j in range(len(sentence2)):
                if sentence1[i].lower() and sentence2[j].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                    if ppdb.presentInPPDB(sentence1[i], sentence2[j], ppdbDict) is True:
                        wordsSimilarity.append([j + 1, t])
            t += 1
        res = []
        for m in range(len(wordsSimilarity)):
            if wordsSimilarity[m] not in res:
                res.append(wordsSimilarity[m])
        return res

def insertAlignPPDB(alignResult, i, cekIdentical, alreadyAlign):
    alreadyAlign.append([])
    tempTidakAda = []
    tempKata = []
    for l in range(len(cekIdentical)):
        tempKata.append(cekIdentical[l][0])
    for j in range(len(alignResult)):
        if alignResult[j][0] not in tempKata:
            tempTidakAda.append(alignResult[j])
    for k in range(len(tempTidakAda)):
        if tempTidakAda[k] not in alreadyAlign[i]:
            temp = [tempTidakAda[k]]
            alreadyAlign[i].extend(temp)
    return alreadyAlign

def removeDuplicate(alreadyAlign, k):
    for i in range(0, len(alreadyAlign[k])):
        for x in range(i + 1, len(alreadyAlign[k])):
            if alreadyAlign[k][i] == alreadyAlign[k][x]:
                alreadyAlign[k].pop(x)
    return alreadyAlign

def isSublist(A, B):
    sub = True
    for item in A:
        if item not in B:
            sub = False
            break
    return sub

def findAllCommonContiguousSublists(A, B, turnToLowerCases=True):
    a = []
    b = []
    for item in A:
        a.append(item)
    for item in B:
        b.append(item)
    if turnToLowerCases:
        for i in range(len(a)):
            a[i] = a[i].lower()
        for i in range(len(b)):
            b[i] = b[i].lower()

    commonContiguousSublists = []
    swapped = False
    if len(a) > len(b):
        temp = a
        a = b
        b = temp
        swapped = True

    maxSize = len(a)
    for size in range(maxSize, 0, -1):
        startingIndicesForA = [item for item in range(0, len(a) - size + 1)]
        startingIndicesForB = [item for item in range(0, len(b) - size + 1)]
        for i in startingIndicesForA:
            for j in startingIndicesForB:
                currentAIndices = [item for item in range(i, i + size)]
                currentBIndices = [item for item in range(j, j + size)]
                alreadyInserted = False
                for item in commonContiguousSublists:
                    if isSublist(currentAIndices, item[0]) and isSublist(currentBIndices, item[1]):
                        alreadyInserted = True
                        break
                if not alreadyInserted:
                    commonContiguousSublists.append([currentAIndices, currentBIndices])
    if swapped:
        for item in commonContiguousSublists:
            temp = item[0]
            item[0] = item[1]
            item[1] = temp

    return commonContiguousSublists

def alignSequences(sentenceLemma1, sentenceLemma2):
    alignments = []
    sourceWordIndicesAlreadyAligned = []
    targetWordIndicesAlreadyAligned = []
    # alignall(>=2)−grammatcheswithatleastonecontentword

    commonContiguousSublists = findAllCommonContiguousSublists(sentenceLemma1, sentenceLemma2, True)
    for item in commonContiguousSublists:
        allStopWords = True
        for jtem in item:
            if jtem not in preprocessing.stopwords and jtem not in preprocessing.punctuations:
                allStopWords = False
                break

    if len(item[0]) >= 2 and not allStopWords:
        for j in range(len(item[0])):
            if item[0][j] + 1 not in sourceWordIndicesAlreadyAligned and item[1][
                j] + 1 not in targetWordIndicesAlreadyAligned and [item[0][j] + 1,
                                                                   item[1][j] + 1] not in alignments:
                # temp = sentenceLemma2[item[1][j]]awal
                # print"belia",item[1][j]
                alignments.append([item[1][j] + 1, item[0][j] + 1])
                sourceWordIndicesAlreadyAligned.append(item[0][j] + 1)
                targetWordIndicesAlreadyAligned.append(item[1][j] + 1)
        return alignments

def textContext(sentence1, sentence2, i, j):
    s1index = []
    s2index = []
    c1 = []
    c2 = []
    for hai in range(len(sentence1)):
        s1index.append([sentence1[hai], hai])
    for hi in range(len(sentence2)):
        s2index.append([sentence2[hi], hi])
    for n in range(1, 4):
        k = i - n
        l = i + n
        if k >= 0:
            if k != i:
                if s1index[k][0].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                    if s1index[k] not in c1:
                        c1.append(s1index[k])
    if l < len(s1index):
        if l != i:
            if s1index[l][0].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                if s1index[l] not in c1:
                    c1.append(s1index[l])

    for o in range(1, 4):
        m = j - o
        y = j + o
        if m >= 0:
            if m != j:
                if s2index[m][0].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                    if s2index[m] not in c2:
                        c2.append(s2index[m])
    if y < len(s2index):
        if y != j:
            if s2index[y][0].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                if s2index[y] not in c2:
                    c2.append(s2index[y])
    context = []
    for mi in range(len(c1)):
        for am in range(len(c2)):
            context.append([c1[mi], c2[am]])
    return context

def alignTextContext(sentence1, sentence2, ppdbDict):
    w = 0.9
    contextSim = 0
    ij = []
    cekaligntextcontext = []
    for i in range(len(sentence1)):
        for j in range(len(sentence2)):
            if sentence1[i].lower() not in preprocessing.stopwords + preprocessing.punctuations and sentence2[j].lower() not in preprocessing.stopwords + preprocessing.punctuations and ppdb.wordSim(sentence1[i], sentence2[j], ppdbDict):
                context = textContext(sentence1, sentence2, i, j)
                for h in range(len(context)):
                    contextSim = contextSim + ppdb.wordSim(context[h][0][0], context[h][1][0], ppdbDict)
                ij.append([i, j, w * ppdb.wordSim(sentence1[i], sentence2[j], ppdbDict) + (1 - w) * contextSim])
    for si in range(len(ij)):
        if ij[si][2] >= w:
            cekaligntextcontext.append([ij[si][1] + 1,
                                        ij[si][0] + 1])
    res = []
    for m in range(len(cekaligntextcontext)):
        if cekaligntextcontext[m] not in res:
            res.append(cekaligntextcontext[m])
    return res

def alignStop(sentence1, sentence2, ppdbDict):
    w = 0.9
    contextSim = 0
    ih = []
    hai = []
    stopaligntextcontext = []
    for i in range(len(sentence1)):
        for j in range(len(sentence2)):
            if sentence1[i].lower() in preprocessing.stopwords and sentence2[j].lower() in preprocessing.stopwords and sentence1[i].lower() == \
                    sentence2[j].lower():
                context = textContext(sentence1, sentence2, i, j)
                for h in range(len(context)):
                    contextSim = contextSim + ppdb.wordSim(context[h][0][0], context[h][1][0], ppdbDict)
                wordSimValue = w * ppdb.wordSim(sentence1[i], sentence2[j], ppdbDict) + (1 - w) * contextSim
                if wordSimValue >= w:
                    ih.append([sentence1[i], sentence2[j], wordSimValue])
                    hai.append([j + 1, i + 1])
                stopaligntextcontext.append([j + 1, i + 1])

    for man in range(len(sentence1)):
        for tap in range(len(sentence2)):
            if sentence1[man].lower() in preprocessing.stopwords and sentence2[tap].lower() in preprocessing.stopwords and sentence1[man].lower() == sentence2[tap].lower():
                if sentence1[man].lower() == sentence2[tap].lower() or ppdb.presentInPPDB(sentence1[man].lower(), sentence2[tap].lower(), ppdbDict):
                    hai.append([tap, man])
    res = []

    for m in range(len(hai)):
        if hai[m] not in res:
            res.append(hai[m])
    return hai

def alignDep(alignDep, ppdbDict):
    parent1 = alignDep[0][0][0]
    POSS = alignDep[0][0][1]
    parent2 = alignDep[1][0][0]
    POST = alignDep[1][0][1]
    child1 = alignDep[0][2][0]
    POSRs = alignDep[0][2][1]
    child2 = alignDep[1][2][0]
    POSRt = alignDep[1][2][1]
    depS = alignDep[0][1]
    depT = alignDep[1][1]

    statS = False
    statT = False
    result = []

    if parent1 == parent2 or ppdb.presentInPPDB(parent1, parent2, ppdbDict):
        # verb verb
        groupOfVerbverb = ['purpcl', 'xcomp']
        if POSS[0] in ['V'] and POSRs[0] in ['V'] and depS in groupOfVerbverb:
            statS = True
        if POST[0] in ['V'] and POSRt[0] in ['V'] and depT in groupOfVerbverb:
            statT = True

    # verb noun
    group1OfVerbnoun = ['agent', 'nsubj', 'xsubj']
    group2OfVerbnoun = ['ccomp', 'dobj', 'nsubjpass ', 'rel', 'partmod']
    group3OfVerbnoun = ['tmod', 'prepin', 'prepat', 'prepon']
    group4OfVerbnoun = ['iobj', 'prepto']

    if POSS[0] in ['V'] and POSRs[0] in ['N'] and depS in group1OfVerbnoun or depS in group2OfVerbnoun or depS in group3OfVerbnoun or depS in group4OfVerbnoun:
        statS = True
    if POST[0] in ['V'] and POSRt[0] in ['N'] and depT in group1OfVerbnoun or depT in group2OfVerbnoun or depT in group3OfVerbnoun or depT in group4OfVerbnoun:
        statT = True

    # noun verb
    groupOfNounverb = ['infmod', 'partmod', 'rcmod']
    if POSS[0] in ['N'] and POSRs[0] in ['V'] and depS in groupOfNounverb:
        statS = True
    if POST[0] in ['N'] and POSRt[0] in ['V'] and depT in groupOfNounverb:
        statT = True

    # noun noun
    groupOfNounnoun = ['pos', 'nn', 'prepof', 'prepin', 'prepat', 'prepfor']
    if POSS[0] in ['N'] and POSRs[0] in ['N'] and depS in groupOfNounnoun:
        statS = True
    if POST[0] in ['N'] and POSRt[0] in ['N'] and depT in groupOfNounnoun:
        statT = True

    # noun adj
    groupOfNounadj = ['amod', 'rcmod']
    if POSS[0] in ['N'] and POSRs[0] in ['J'] and depS in groupOfNounadj:
        statS = True
    if POST[0] in ['N'] and POSRt[0] in ['J'] and depT in groupOfNounadj:
        statT = True
    if statS == True and statT == True:
        result.append(alignDep)
    else:
        print("c")

    # verb verb
    group1OfOppositeVerbverb = ['conjand']
    group2OfOppositeVerbverb = ['conjor']
    group3OfOppositeVerbverb = ['conjnor']
    if POSS[0] in ['V'] and POSRs[0] in ['V'] and depS in group1OfOppositeVerbverb or depS in group2OfOppositeVerbverb or depS in group3OfOppositeVerbverb:
        statS = True
    if POST[0] in ['V'] and POSRt[0] in ['V'] and depS in group1OfOppositeVerbverb or depS in group2OfOppositeVerbverb or depS in group3OfOppositeVerbverb:
        statT = True

    # verb noun
    groupOfOppositeVerbnoun = [['ccomp', 'dobj', 'nsubjpass', 'rel', 'partmod'], ['nfmod', 'partmod', 'rcmod']]
    if POSS[0] in ['V'] and POSRs[0] in ['N'] and depS in groupOfOppositeVerbnoun[0]:
        statS = True
    if POST[0] in ['V'] and POSRt[0] in ['N'] and depT in groupOfOppositeVerbnoun[1]:
        statT = True

    # verb adj
    groupOfOppositeVerbadj = [['acomp'], ['cop', 'csubj']]
    if POSS[0] in ['V'] and POSRs[0] in ['J'] and depS in groupOfOppositeVerbadj[0]:
        statS = True
    if POST[0] in ['V'] and POSRt[0] in ['J'] and depT in groupOfOppositeVerbadj[1]:
        statT = True

    # noun noun
    group1OfOppositeNounnoun = ['conjand']
    group2OfOppositeNounnoun = ['conjor']
    group3OfOppositeNounnoun = ['conjnor']
    if POSS[0] in ['N'] and POSRs[0] in ['N'] and depS in group1OfOppositeNounnoun or depS in group2OfOppositeNounnoun or depS in group3OfOppositeNounnoun:
        statS = True
    if POST[0] in ['N'] and POSRt[0] in ['N'] and depS in group1OfOppositeNounnoun or depS in group2OfOppositeNounnoun or depS in group3OfOppositeNounnoun:
        statT = True

    # nounadj
    groupOfOppositeNounadj = [['amod', 'rcmod'], ['nsubj']]
    if POSS[0] in ['N'] and POSRs[0] in ['J'] and depS in groupOfOppositeNounadj[0]:
        statS = True
    if POST[0] in ['N'] and POSRt[0] in ['J'] and depT in groupOfOppositeNounadj[1]:
        statT = True

    # adj adj
    group1OfOppositeAdjadj = ['conjand']
    group2OfOppositeAdjadj = ['conjor']
    group3OfOppositeAdjadj = ['conjnor']
    if POSS[
        0] in ['J'] and POSRs[0] in ['J'] and depS in group1OfOppositeAdjadj or depS in group2OfOppositeAdjadj or depS in group3OfOppositeAdjadj:
        statS = True
    if POST[
        0] in ['J'] and POSRt[0] in ['J'] and depT in group1OfOppositeAdjadj or depT in group2OfOppositeAdjadj or depT in group3OfOppositeAdjadj:
        statT = True

    # adv adv
    group1OfOppositeAdvadv = ['conjand']
    group2OfOppositeAdvadv = ['conjor']
    group3OfOppositeAdvadv = ['conjnor']
    if POSS[0] in ['R'] and POSRs[0] in ['R'] and depS in group1OfOppositeAdvadv or depS in group2OfOppositeAdvadv or depS in group3OfOppositeAdvadv:
        statS = True
    if POST[0] in ['R'] and POSRt[0] in ['R'] and depT in group1OfOppositeAdvadv or depT in group2OfOppositeAdvadv or depT in group3OfOppositeAdvadv:
        statT = True
    if statS == True and statT == True:
        result.append(alignDep)
    return result

def selectDep(sourcedep, targetdep, ppdbDict):
    aligndep = []
    for t in range(len(sourcedep)):
        for r in range(len(targetdep)):
            if sourcedep[t][0][0] == targetdep[r][0][0] and sourcedep[t][2][0] == targetdep[r][2][0] or \
                    sourcedep[t][0][0] == targetdep[r][2][0] and sourcedep[t][2][0] == targetdep[r][0][0] or \
                    ppdb.presentInPPDB(sourcedep[t][0][0], targetdep[r][0][0], ppdbDict) and ppdb.presentInPPDB(sourcedep[t][2][0], targetdep[r][2][0], ppdbDict) or \
                    ppdb.presentInPPDB(sourcedep[t][0][0],targetdep[r][2][0], ppdbDict) and ppdb.presentInPPDB(sourcedep[t][2][0], targetdep[r][0][0], ppdbDict):
                aligndep.append([sourcedep[t],targetdep[r]])
    return aligndep


def alignDepContext(sentence1, sentence2):
    alignDependency = []

    alignDependencyf = []
    dep1 = tools.depParser(sentence1)
    dep2 = tools.depParser(sentence2)
    sourcedep = []
    targetdep = []
    for k in range(len(dep1[0])):
        if dep1[0][k][0][1][0] in ['V', 'N', 'J', 'R'] and dep1[0][k][2][1][0] in ['V', 'N', 'J', 'R']:
            sourcedep.append(dep1[0][k])
            for l in range(len(dep2[0])):
                if dep2[0][l][0][1][0] in ['V', 'N', 'J', 'R'] and dep2[0][l][2][1][0] in ['V', 'N', 'J', 'R']:
                    targetdep.append(dep2[0][l])

    aligndepend = selectDep(sourcedep, targetdep)
    depTemp = []
    for e in range(len(aligndepend)):
        yoho = alignDep(aligndepend[e])
        if yoho:
            depTemp.extend(yoho)

    for t in range(len(depTemp)):
        # word1S = depTemp[t][0][0][0]
        # word2S = depTemp[t][0][2][0]
        word1T = depTemp[t][1][0][0]
        word2T = depTemp[t][1][2][0]

        for g in range(len(sentence1)):
            for gi in range(len(sentence2)):
                if word1T == sentence1[g] and word1T == sentence2[gi] and word1T not in preprocessing.stopwords + preprocessing.punctuations:
                    alignDependency.append([gi + 1, g + 1])

    for f in range(len(sentence1)):
        for fi in range(len(sentence2)):
            if word2T == sentence1[f] and word2T == sentence2[fi] and word2T not in preprocessing.stopwords + preprocessing.punctuations:
                alignDependency.append([fi + 1, f + 1])
    res = []

    for m in range(len(alignDependency)):
        if alignDependency[m] not in res:
            res.append(alignDependency[m])
    return res

def alignWordSimilarityex(sentence1, sentence2, ppdbDictex):
    wordsSimilarity = []
    t = 1

    # one to one
    for i in range(len(sentence1)):
        for j in range(len(sentence2)):
            if sentence1[i].lower() and sentence2[j].lower() not in preprocessing.stopwords + preprocessing.punctuations:
                if ppdb.presentInPPDBex(sentence1[i], sentence2[j], ppdbDictex) is True:
                    # masukkan indeks kata dan katanya
                    wordsSimilarity.append([j + 1, t])
        t += 1

    # two to two
    for mu in range(len(sentence1) - 1):
        for nu in range(len(sentence2) - 1):
            temp1 = sentence1[mu].lower() + ' ' + sentence1[mu + 1].lower()
            temp2 = sentence2[nu].lower() + ' ' + sentence2[nu + 1].lower()
            if ppdb.presentInPPDBex(temp1, temp2, ppdbDictex) is True:
                wordsSimilarity.append([nu + 1, mu + 1])
                wordsSimilarity.append([nu + 2, mu + 2])

    # two to one

    for ni in range(len(sentence1) - 1):
        for pu in range(len(sentence2) - 1):
            tem1 = sentence1[ni].lower() + '  ' + sentence1[ni + 1].lower()
            tem2 = sentence2[pu].lower()
            te1m = sentence1[ni].lower()
            te2m = sentence2[pu].lower() + '  ' + sentence2[pu + 1].lower()
            if ppdb.presentInPPDBex(tem1, tem2, ppdbDictex) is True:
                wordsSimilarity.append([pu + 1, ni + 1])
                wordsSimilarity.append([pu + 1, ni + 2])
                if ppdb.presentInPPDBex(te1m, te2m, ppdbDictex) is True:
                    wordsSimilarity.append(([pu + 1, ni + 1]))
                    wordsSimilarity.append([pu + 2, ni + 1])

    # three to one

    for ni in range(len(sentence1) - 2):
        for pu in range(len(sentence2) - 2):
            tem1 = sentence1[ni].lower() + ' ' + sentence1[ni + 1].lower() + ' ' + sentence1[ni + 2].lower()

            tem2 = sentence2[pu].lower()
            te1m = sentence1[ni].lower()

            te2m = sentence2[pu].lower() + ' ' + sentence2[pu + 1].lower() + ' ' + sentence2[pu + 2].lower()
            if ppdb.presentInPPDBex(tem1, tem2, ppdbDictex) is True:
                wordsSimilarity.append([pu + 1, ni + 1])
                wordsSimilarity.append([pu + 1, ni + 2])
                wordsSimilarity.append([pu + 1, ni + 3])
                if ppdb.presentInPPDBex(te1m, te2m, ppdbDictex) is True:
                    wordsSimilarity.append(([pu + 1, ni + 1]))
                    wordsSimilarity.append([pu + 2, ni + 1])
                    wordsSimilarity.append(([pu + 3, ni + 1]))
    return wordsSimilarity