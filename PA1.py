# -*- coding: utf-8 -*-
import itertools
import string
"""
Corinne Bintz
Programming Assignment 1
Sample Output:
deduce(["(A and C) or not D", "(B or C) and (D or A)",...
"(not C and B) or (not D and not B)"])
C D B A 
--------
T F F T 
F F T T 

Approximate time spent: 8 hours
"""

def varList(inputList):
    """
    Input: a list of strings that contain logical predicates
    Output:a list of the variables with no duplicates 
    """
    VL=[]
    for predicate in inputList: 
        for character in predicate: 
            if character not in VL: 
                if character in string.ascii_uppercase: 
                    VL.append(character) 
    return VL
            
def trueFalseCombo(varsList):
    """
    Input: a list of variables 
    Output: a list all of the possible combinations of True and False with the 
    given number of variables
    """
    numVars = len(varsList)
    table =  list(itertools.product([True, False], repeat=numVars))
    return table 

def assignVar(varsList, trueFalseCombos):
    """
    Input: a list of variables and a list of true/false combinations
    Function: Assigns each variable a list of its conditions (true or
    false) for each combination in the list of true/false combinations
    """
    for varIndex in range(len(varsList)): 
        varsList[varIndex] = []
        for comboIndex in range(len(trueFalseCombos)):
            varsList[varIndex].append(trueFalseCombos[comboIndex][varIndex])


def makeVarDict(varsList, trueFalseCombos, comboIndex):
    """
    Input: a list of the variables, a list of the true/false combinations, 
    and an integer (combIndex) which tells us which index we are on in the list
    of true/false combinations
    Ouput: a dictionary with variables as keys and their assigned condition 
    (true or false) as values
    """
    varDict = {}
    for index in range(len(varsList)):
        varDict[varsList[index]] = trueFalseCombos[comboIndex][index]
    return varDict
    
def printVars(dictionary):
    """"
    Input: a dictionary with variable, condition as key, value pairs
    Function: prints a line with all of the variables 
    """
    for var, condition in dictionary.items():
        print(var, end =" ")
    print("")

def printConditions(dictionary):
    """"
    Input: a dictionary with variable, condition as key, value pairs
    Function: prints a line with all of the conditions as T (true) or F (false) 
    """
    for var, condition in dictionary.items():
        if condition==True:
            print("T", end=" ")
        else:
            print("F", end= " ")
    print("")
    
def deduce(s):
    """"
    Input: a list of strings that contain logical predicates
    Output: a list of assignments of the variables such that all predicates 
    in the input list are true.
    """
    deduceComboList = []
    myVarList = varList(s)
    myTrueFalseCombos = trueFalseCombo(myVarList)
    for comboIndex in range(len(myTrueFalseCombos)):
        count = 0
        for predicate in s:
            if eval(predicate, makeVarDict(myVarList, myTrueFalseCombos, 
                                           comboIndex)) == True:
                count+=1
        if count == len(s):
            deduceComboList.append(makeVarDict(myVarList, myTrueFalseCombos, 
                                               comboIndex))
    # the variables are the same for each dictionary in the deduceComboList so
    # we just print the variables in the first dictionary
    printVars(deduceComboList[0]) 
    
    #print break line of appropriate size
    for index in range(2*len(myVarList)-1):
        print("-", end = "")
    print("")
    
    # but, the condition assignments are different for each dictionary in the 
    # deduceComboList so we need to print the condition assignments for each 
    # dictionary in the deduceComboList
    for possibleCombo in deduceComboList:
        printConditions(possibleCombo)
    

            
              
                
             
                