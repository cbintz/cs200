"""
Corinne Bintz
Programming Assignment 2
Worked with Ben Slater
6 hours
Sample output:
>>> BFS('CSCI 0101')
Reachable from CSCI 0101: 
['CSCI 0101', 'CSCI 0200', 'CSCI 0201', 'CSCI 0202', 'CSCI 0301', 'CSCI 0302', 'CSCI 0311', 'CSCI 0312', 'CSCI 0313', 'CSCI 0314', 'CSCI 0315', 'CSCI 0390', 'CSCI 0413',
'CSCI 0414', 'CSCI 0431', 'CSCI 0433', 'CSCI 0441', 'CSCI 0451', 'CSCI 0452', 'CSCI 0453', 'CSCI 0454', 'CSCI 0461', 'CSCI 0463', 'CSCI 0465', 'CSCI 0466', 'CSCI 1005']
Uneachable from CSCI 0101: 
['CSCI 0150', 'CSCI 0190', 'CSCI 0321', 'CSCI 0333', 'CSCI 0500', 'CSCI 0701', 'CSCI 0702', 'CSCI 1004', 'CSCI 1011']

"""
from bs4 import BeautifulSoup
import requests
import string
import queue

def getPage(url):
    """
    Input: url
    Output: page content (data from CS courses website)
    """
    page = requests.get(url)
    return page.content

def makeAdjacencyList(page):
    """
    Input: data from CS courses website
    Output: preReqDict, a dictionary that represents the adjacency list for the directed graph where each CSCI class is a vertex
    and we put an edge between two classes if one class is a prereq for the other.
    """
    courses = [] # list of all CSCI courses
    courseDescs = [] # list of all CSCI course descriptions
    courseDict = {} # dictionary with courses as keys and course descriptions as values
    preReqDict = {} # dictionary with courses as keys and the courses that take that course as a prereq 
    soup = BeautifulSoup(page, 'html.parser')
    
    for link in soup.find_all("h5"): 
        courses.append(link.text[0:9]) # make courses list
    
    for item in soup.find_all("div", attrs = {"class":"coursedesc"}): # make course descriptions list
        courseDescs.append([item.text])
          
    for index in range(len(courses)):
        courseDict[courses[index]] = courseDescs[index] # match courses with course descriptions to make course dictionary

    for course in courseDict: # make initial preReqDict with courses as keys and empty lists as values
        preReqDict[course] = []

    for course, desc in courseDict.items(): # first iteration so we can use course as key for preReqDict
        for course1, desc1 in courseDict.items(): # second iteration so we can determine if course1 takes course as a pre req
            if any(course in s for s in desc1):
                preReqDict[course].append(course1) # if course1 takes course as a prereq, add course1 to course's value list
            if any('One CSCI course at the 0100-level' in s for s in desc1): # special exception for 100-level courses
                if not any(course1 in s for s in preReqDict['CSCI 0101']):  # to avoid overcounting
                    preReqDict['CSCI 0101'].append(course1)
                if not any(course1 in s for s in preReqDict['CSCI 0150']):  # to avoid overcounting
                    preReqDict['CSCI 0150'].append(course1)
                if not any(course1 in s for s in preReqDict['CSCI 0190']):  # to avoid overcounting
                    preReqDict['CSCI 0190'].append(course1)
            if course1 == 'CSCI 0321':
                preReqDict['CSCI 0201'].append(course1) # account for typo of 0201 as 201 in 321's course description
    
    return preReqDict

def BFS(s):
    """
    Function: Breadth-first-search of out prereq graph
    Input: s, our starting vertex
    Output: Prints a list of courses reachable from starting vertex and a list of courses unreachable from starting vertex
    """
    page = getPage("http://www.middlebury.edu/academics/cs/courses")
    preReqDict = makeAdjacencyList(page)
    reachableList = []
    unreachableList = []
    Exp = {} # dictionary with vertices as keys and value = 0 if vertex has been explored and value = 1 if not
    for course in preReqDict:
        Exp[course] = 0
    A = queue.Queue()
    A.put(s)
    Exp[s] = 1
    while A.empty()!= True:
        v = A.get()
        for edge in preReqDict[v]:
            if Exp[edge] == 0:
                A.put(edge)
                Exp[edge] = 1
    for vertex in Exp:
        if Exp[vertex] ==1: # add explored values to reachable list
            reachableList.append(vertex)
        else:               # add unexplored values to unreachable list
            unreachableList.append(vertex)
    print("Reachable from " + s + ": ")
    print(reachableList)
    print("Uneachable from " + s + ": ")
    print(unreachableList)
    
