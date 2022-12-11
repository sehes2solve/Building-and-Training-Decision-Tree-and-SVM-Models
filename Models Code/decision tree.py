import math, random, copy
import numpy as np
import matplotlib.pyplot as plt


class Node:
    def __init__(self):
        self.answer = -1
        self.attributeIdx = -1
        self.attributeVal = -1
        self.children = []


def getLog(num):
    if (num == 0):
        return 0
    return math.log(num, 2)


def getEntropy(currentVotes, index, party):
    # [number of republicans,number of democrats]
    Ys = [0, 0]
    Ns = [0, 0]
    for i in range(0, len(currentVotes)):
        if (currentVotes[i][index] == 'y'):
            if (party[i][0] == 'r'):
                Ys[0] += 1
            else:
                Ys[1] += 1
        else:
            if (party[i][0] == 'r'):
                Ns[0] += 1
            else:
                Ns[1] += 1
    cntOfYs = Ys[0] + Ys[1]
    cntOfNs = Ns[0] + Ns[1]
    sum = cntOfNs + cntOfYs

    YsEntropy = -Ys[0] * getLog(Ys[0]) - Ys[1] * getLog(Ys[1])

    NsEntropy = -Ns[0] * getLog(Ns[0]) - Ns[1] * getLog(Ns[1])
    return (cntOfNs / sum) * NsEntropy + (cntOfYs / sum) * YsEntropy


def getBestAttributeInd(currentVotes, party):
    bstInd = -1
    currentEntropy = math.inf
    for i in range(0, len(currentVotes[0])):
        entropy = getEntropy(currentVotes, i, party)
        if (entropy < currentEntropy):
            bstInd = i
            currentEntropy = entropy
    return bstInd


# returns true if party list contains the party for all of the items
def checkIfEnd(party, currentVotes):
    if (len(currentVotes[0]) == 0):
        return True
    for i in range(1, len(party)):
        if (party[i] != party[i - 1]):
            return False
    return True


# todo delete this method
def checkIfBad(votes):
    for i in range(1, len(votes)):
        if (len(votes[i]) != len(votes[i - 1])):
            return True
    return False


def solve(node, currentVotes, party):
    if (checkIfEnd(party, currentVotes)):
        node.answer = party[0]
        return
    bstAttribute = getBestAttributeInd(currentVotes, party)
    node.attributeIdx = bstAttribute
    Ys = []
    partyYs = []
    Ns = []
    partyNs = []
    for i in range(0, len(currentVotes)):
        currentItem = currentVotes[i].copy()
        del currentItem[bstAttribute]
        if (currentVotes[i][bstAttribute] == 'y'):
            Ys.append(currentItem)
            partyYs.append(party[i])
        else:
            Ns.append(currentItem)
            partyNs.append(party[i])
    if (len(Ys) > 0):
        newNode = Node()
        newNode.attributeVal = 'y'
        node.children.append(newNode)
        solve(newNode, Ys, partyYs)
    if (len(Ns) > 0):
        newNode = Node()
        newNode.attributeVal = 'n'
        node.children.append(newNode)
        solve(newNode, Ns, partyNs)


def fixVotesByCol(votes):
    for i in range(0, len(votes[0])):
        Ys = 0
        Ns = 0
        for j in range(0, len(votes)):
            if (votes[j][i] == 'y'):
                Ys += 1
            else:
                Ns += 1
        bstVote = 'y'
        if (Ns > Ys):
            bstVote = 'n'
        for j in range(0, len(votes)):
            if (votes[j][i] == '?'):
                votes[j][i] = bstVote
def fixVotesByRow(votes):
    for i in range(0,len(votes)):
        ys=0
        ns=0
        for j in range(0,len(votes[i])):
            if(votes[i][j]=='y'):
                ys+=1
            elif(votes[i][j]=='n'):
                ns+=1
        maj='y'
        if(ns>ys):
            maj='n'
        for j in range(0,len(votes[i])):
            if(votes[i][j]=='j'):
                votes[i][j]=maj

def getExpectedAnswer(voteStreak, node):
    if (node.attributeIdx == -1):
        return node.answer
    voteAnswerAtCurrentAttribute = voteStreak[node.attributeIdx]
    for i in range(0, len(node.children)):
        if (voteAnswerAtCurrentAttribute == node.children[i].attributeVal):
            return getExpectedAnswer(voteStreak, node.children[i])
    return 'bad'


def getAccuracy(votes, party, node):
    correctExamples = 0
    for i in range(0, len(votes)):
        ans = getExpectedAnswer(votes[i], node)
        if (ans == party[i]):
            correctExamples += 1
    return correctExamples / len(votes)


def getTreeSize(node):
    ans = 1
    for i in range(0, len(node.children)):
        ans += getTreeSize(node.children[i])
    return ans


def solveFiveTimes(initVotes, party, TrainingCount):
    lst = [i for i in range(0, len(party))]
    ans = []
    treeSzs = []
    for i in range(0, 5):
        random.shuffle(lst)
        # lst = [2,0,4,1,3] random permutation
        currentTrainingVotes = []
        currentTrainingParty = []
        for j in range(0, TrainingCount):
            currentTrainingVotes.append(initVotes[lst[j]])
            currentTrainingParty.append(party[lst[j]])
        currentTestingVotes = []
        currentTestingParty = []
        for j in range(TrainingCount, len(party)):
            currentTestingVotes.append(initVotes[lst[j]])
            currentTestingParty.append(party[lst[j]])
        node = Node()
        solve(node, currentTrainingVotes
              , currentTrainingParty)
        treeSzs.append(getTreeSize(node))
        ans.append(getAccuracy(currentTestingVotes, currentTestingParty, node))
    return ans, treeSzs
def getMaxMinAvg(lst):
    mx=0
    mn=math.inf
    avg=0
    for i in range(0,len(lst)):
        mx=max(mx,lst[i])
        mn=min(mn,lst[i])
        avg+=lst[i]
    avg/=len(lst)
    return mx,mn,avg

# /////////

# //////
file = open("inp.txt", "r")
party = []
votes = []
for line in file:
    # deleting the \n from line string
    line = line[:-1]
    line = line.split(',')
    party.append(line[0])
    votes.append(line[1:])
fixVotesByRow(votes)


for i in range(30, 80, 10):
    trainSize = (i / 100) * len(votes)
    res = solveFiveTimes(votes, party, int(trainSize))
    print("for training data of "+str(i)+"% = ",end='')
    accurracy = getMaxMinAvg(res[0])
    treeSz = getMaxMinAvg(res[1])
    print(str(accurracy[0])+" "+str(accurracy[1])+" "+str(accurracy[2])+" "+str(treeSz[0])+" "+str(treeSz[1])+" "+str(treeSz[2]))
