from secrets import choice


def getWords(data, scale):
    source = open(data,"r")
#     solution = list()
    firstWords = list()
    for w in source:
        ww = w.strip()
#         solution.append(ww)
        if len(ww)==scale:
            firstWords.append(ww)
    return firstWords

import random
def frequenChoi(bank):
    abc = [[chr(i+97),0] for i in range(26)]
    for w in bank:
        for w1 in w:
            abc[ord(w1)-97][1] += 1
    abc.sort(key = lambda s: s[1] , reverse = True)
    bank2 = bank.copy()
    for i in range(5):
        tmp = list()
        for w in bank2:
            if abc[i][0] in w:
                tmp.append(w)
        if len(tmp) == 0:
            bankChoi = random.choice(bank2)
            return bankChoi
        bank2.clear()
        bank2 = tmp.copy()
    bankChoi = random.choice(bank2)
    return bankChoi

def update2(bank,color,guess):
    zerocon=[0]*5
    twocon=[0]*5
    for i in range(5):
        if color[i]==0:
            ct1=0
            for j in range(5):
                if guess[i]==guess[j] and color[j]!=0:
                    ct1+=1;
            zerocon[i]=ct1
        if color[i]=="2":
            ct2=0
            for j in range(5):
                if guess[i]==guess[j] and j<i and color[j]==2:
                    ct2=0
                    break
                elif guess[i]==guess[j] and color[j]==0:
                    ct2=0
                    break
                elif guess[i]==guess[j]:
                    ct2+=1
            twocon[i]=ct2
    lenght=len(bank)
    delete=[0]*lenght
    for w in range(lenght):
        for i in range(5):
            if color[i]==1 and bank[w][i]!=guess[i]:
                delete[w]=1
                break
                
            elif color[i]==0:
                if bank[w][i]==guess[i]:
                    delete[w]=1
                    break
                if zerocon[i]>0:
                    counter=0
                    for j in range(5):
                        if bank[w][j]==guess[i]:
                            counter+=1
                    if counter!=zerocon[i]:
                        delete[w]=1
                        break
                else:
                    for j in range(5):
                        if bank[w][j]==guess[i]:
                            delete[w]=1
                            break
                    
            elif color[i]==2:
                if bank[w][i] == guess[i]:
                    delete[w]=1
                    break
                if twocon[i]>0 :
                    counter2=0
                    for j in range (5):
                        if bank[w][j] == guess[i]:
                            counter2+=1
                    if counter2<twocon[i]:
                        delete[w]=1
                        break
    newbank = list()
    for w in range(lenght):
        if delete[w]==0:
            newbank.append(bank[w])
    return newbank

def getColor(guess,ans):
    color = list()
    ansAvai = [1] * 5
    for i in range(5):
        if guess[i] == ans[i]:
            color.append(1)
            ansAvai[i] = 0 
        else:
            check = 1
            for j in range(5):
                if guess[i] == ans[j] and ansAvai[j] and guess[j] != ans[j]:
                    color.append(2)
                    ansAvai[j] = 0 
                    check = 0
                    break
            if check:
                color.append(0)
    return color

import sys
dicFile = sys.argv[1]
testFile = sys.argv[2]
outputFile = sys.argv[3]

scale = 5
allWords = getWords(dicFile, scale)
test = getWords(testFile, scale)

outF = open(outputFile,"w")
sumStep = 0
for w in test:
    outF.write(w+'\n')
    bank = allWords.copy()
    step = 0
    for ii in range(10):
        guess = frequenChoi(bank)
        color = getColor(guess,w)
        colorStr = "\""
        for i in range(scale):
            colorStr += str(color[i])
            if i != scale - 1:
                colorStr += ","
            else:
                colorStr += "\""
#         print(guess,color,colorStr)
        outF.write(str(step+1)+"; "+guess+"; "+colorStr+'\n')
#         print(str(step+1)+"; "+guess+"; "+colorStr+'\n')
        if colorStr == "\"1,1,1,1,1\"":
            break
        bank = update2(bank,color,guess)
#         print('\n',bank)
        step += 1
    outF.write(str(step+1)+'\n')
    sumStep += (step+1)
outF.write('\n'+"sum step = "+str(sumStep))
outF.close()