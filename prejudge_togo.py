#!/usr/bin/env python
# coding: utf-8

# #### Introduction to Artificial Intelligence @ cs.nccu.edu.tw
# ##### File: prejudge.ipynb
# ##### Prepared by: Chao-Lin Liu
# ##### Date: 25 April 2022
# ##### Purpose:
# #####     Check the output of competitors' Wordle solvers
# #####         1 If the output is perfect, an intermediate file will be generated to contain the guessing results
# ######             1.1 The output files of all competitors will be combined for a tournament
# #####         2 If the output is defective, errors will be identifed and reported

def getWords(data, scale):
    source = open(data,"r")
    solution = list()
    firstWords = list()
    for w in source:
        ww = w.strip()
        solution.append(ww)
        if len(set(ww))==scale:
            firstWords.append(ww)
    return solution, firstWords

def valid(word, answers):
    return (word in answers)

def compare2words(answer, guess):
    la = list(answer)
    lg = list(guess)
    results = [0] * len(la)
    matched = [0] * len(la)
    for i in range(len(lg)):
        if (lg[i]==la[i]):
            matched[i] = 1  # 1 for used
            results[i] = 1  # 1 for "A"
    for i in range(len(lg)):
        if (results[i]>0):
            continue
        for j in range(len(la)):
            if (matched[j]>0):
                continue
            if (lg[i]==la[j]):
                matched[j] = 1  # 1 for used
                results[i] = 2  # 2 for "B"
                break
    return results

def parseLine(answers, currentAns, line, first=-1):
    print(line.strip())
    parts = line.strip().split(";")
    status = True
    if not parts[0].isdigit():
        print ("Error: this line must start with a number: \n {}".format(line.strip()))
        status = False
    elif int(parts[0])!= first:
        print("Error: this line should start with {:d}: \n {}".format(first,line.strip()))
        status = False
    myAns = parts[1].strip()
    validGuess = valid(myAns, answers)
    if not validGuess:
        print("Error: "+myAns+" is not a valid answer.")
        status = False
    else:
        correctness = compare2words(currentAns, myAns)
        
    raw = parts[2].strip()
    if raw.find("\'"):
        subs = raw.split(",")
        newsubs = [int(x.strip().replace("\"","")) for x in subs]
    else:
        subs = raw.split(",")
        newsubs = [int(x.strip().replace("\'","")) for x in subs]

    if validGuess and (correctness!=newsubs):
        print("Error: wrong color codes: {} in {}".format(str(newsubs), line.strip()))
        status = False

    if (myAns==currentAns) and (newsubs!=len(currentAns)*[1]):
        print("Error: please make sure the answer is perfect: "+line.strip())
        status = False
        
    perfect = newsubs==len(currentAns)*[1]
        
    return status, perfect

def prejudge(teamRec, answerSet):
    responses = open(teamRec,"r")
    results = open(teamRec[:-4]+"_Checked.txt", "w")
    verified = True
    perfect = False
    finalCount = -1
    for aLine in responses:
        text = aLine.strip()
        if text[0].islower():
            print("\n"+aLine.strip())
            lines = 0
            verified = True
            perfect = False
            goal = aLine.strip()
        elif text.isdigit():
            if not perfect:
                print("Error: You cannot report the counts unless the last trial is perfect: "+text)
                verified = False
            trials = int(text)
            finalCount = -1
            if (trials != lines):
                print("Error: Incorrect final count of trials")
                print("       Your records indicate {:d} times.".format(lines))
                verified = False
            else:
                finalCount = trials
                if verified:
                    results.write(goal+","+str(finalCount)+"\n")
        else:
            lines = lines + 1
            print("normal lines")
            nextStep, perfect = parseLine(answerSet, goal, aLine, lines)
            verified = verified and nextStep
    responses.close()
    results.close()

def main(responses, answerFile):
#    answerFile = "wordle-answers-alphabetical.txt"
    scale = 5
    answerSet, _ = getWords(answerFile, scale)
#    prejudge("team0_buggy.txt", answerSet)
#    prejudge("team0_first.txt", answerSet)
    prejudge(responses, answerSet)

import sys
if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv)!=3:
        print("Error")
        sys.exit(0)
    responses = sys.argv[1]
    answerFile = sys.argv[2]
    main(responses, answerFile)
