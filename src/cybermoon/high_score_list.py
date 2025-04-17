import os
import json


class HighScoreList:

    def __init__(self, maxElem):

        self.maxElements = maxElem  # capacity of list
        self.nameList = []  # list of names
        self.scoreList = []  # list of scores

    def addName(self, name, score):
        # adds a new name and score to
        # the variables 'self.nameList' and 'self.scoreList'

        self.nameList.append(name)
        self.scoreList.append(score)
        if len(self.nameList) > self.maxElements:
            # remove the lowest score at the end after sorting
            self.nameList.pop()
            self.scoreList.pop()
        self.sortList()

    def sortList(self):
        # sorts the list in descending order according to the scores
        combined = zip(self.scoreList, self.nameList)
        sorted_combined = sorted(combined, reverse=True)
        self.scoreList, self.nameList = map(
            list, zip(*sorted_combined)
        )  # convert back to lists

    def compareToList(self, yourScore):
        # compares yourScore to the scores in the list to find the rank
        tempScoreList = list(self.scoreList)  # convert to list if it's not already
        tempScoreList.append(yourScore)
        tempScoreList.sort(reverse=True)
        return tempScoreList.index(yourScore) + 1  # adding 1 for 1-based indexing

    def saveToFile(self, fileName):
        # save the high score list
        if len(self.nameList) > 0 and len(self.scoreList) > 0:
            with open(fileName, "w") as file:
                json.dump({"names": self.nameList, "scores": self.scoreList}, file)

    def fileExists(self, fileName):
        # check if the high score file exists
        return os.path.exists(fileName)

    def loadFromFile(self, fileName):
        # load the high score list
        if self.fileExists(fileName):
            # print("High scores loaded")
            with open(fileName, "r") as file:
                data = json.load(file)
                self.nameList = data["names"]
                self.scoreList = data["scores"]
                self.sortList()  # ensure the list is sorted after loading
