from random import *
from math import log
'''
3 approaches: naive_compare, compare, and just straight addition
'''
# Creates an adversary for predicting human behavior

def generate(n, deg):
    running_str = "000"
    counts = {}
    for i in range(n-deg+1):
        predictor =  running_str[-deg:]
        if predictor in counts.keys():
            zeds = counts[predictor][0]
            ones = counts[predictor][1]
            if zeds >= ones:
                running_str += "1"
                counts[predictor][1] += 1
            else: 
                running_str += "0"
                counts[predictor][0] +=1
        else: 
            counts[predictor] = [0,1]
            running_str += "1"
    return running_str

def guesser(s):
    correct = 1.5
    running_str = s[:3]
    wrong = 1.5
    counts = {}
    ind = 3
    while ind <= len(s)-1:
        predictor = running_str[-3:]
        if predictor in counts.keys():
            zeds = counts[predictor][0]
            ones = counts[predictor][1]
            if zeds > ones:
                #guesszeds
                if s[ind] == "0":
                    correct += 1
                    counts[predictor][0] += 1
                else:
                    wrong += 1
                    counts[predictor][1] += 1
                running_str += s[ind]
            elif ones > zeds:
                if s[ind] == "1":
                    correct += 1
                    counts[predictor][1] += 1
                else:
                    wrong += 1
                    counts[predictor][0] += 1
                running_str += s[ind]
            else:
                correct += 0.5
                wrong += 0.5
                counts[predictor][int(s[ind])] += 1
                running_str += s[ind]
        else:
            counts[predictor] = [0,1]
            running_str += s[ind]
        ind += 1
    return (correct/(correct + wrong))
        

def naive_compare(a, b, c, d):
    if a == c and b == d:
        return randint(0,1)
    elif a/b > c/d:
        return 0
    elif c/d > a/b:
        return 1
    elif c > a:
        return 1
    return 0
    
def compare(a, b, c, d):
    #if we have a successes out of b times and c successes out of d times, what are we more "sure" of?
    #simple mathematical model gives the following
    if a+d-c > b+c-a:
        return 0 #a/b is better
    elif b+c-a > a+d-c:
        return 1 #b/c is better
    return randint(0,1)

def evalpos(a, b):
    #translate a/b into some sort
    return a/(b) * log(b, 2)
def evalneg(a, b):
    return (b-a)/(b) * log(b, 2)

def human_predictor(st, degmin, degmax):
    #sensitivity = deg; measures up to prev. deg digits
    successes = 0
    totals = 0
    ind = 0
    prefixes = {}
    k = randint(0,1)
    if k == st[ind]:
        successes += 1
    ind += 1
    while ind <= len(st)-1:
        #after adding a character, add the prefixes before it
        char = int(st[ind])
        pres = []
        for i in range(degmin, min(degmax, ind)+1):
            pres.append(st[ind-i:ind])
        p0 = 0
        p1 = 0
        #print("relevant:", pres)
        for j in pres:
            #add half of the probability to p1
            if j not in prefixes.keys():
                prefixes[j] = [0,0]
                p1 += 1/2
                p0 += 1/2
            else:
                p1 += evalpos(prefixes[j][1], prefixes[j][0] + prefixes[j][1])
                p0 += evalneg(prefixes[j][1], prefixes[j][0] + prefixes[j][1])
        print(prefixes)
        #print(p1)
        if p1 > p0:
            #guess 1
            if char == 1:
                successes += 1
        elif p1 < p0:
            if char == 0:
                successes += 1
        else:
            guess = randint(0,1)
            if char == guess:
                successes += 1
        #need to update prefixes
        for j in pres:
            prefixes[j][int(char)] += 1
        totals += 1
        ind += 1
    print(successes, totals)

            
            
                
    
        
    
