import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QTableWidget
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt



firstEntry = 0

# Creating the Window
app = QApplication([])
window = QWidget()
window.setWindowTitle("Aleks Le Fan Data Processor")
font = QFont("Comic Sans MS", 16)

grid = QGridLayout()
table = QTableWidget()

window.setLayout(grid)
grid.addWidget(table, 0, 0)

sys.exit(app.exec())


# Functions for AleksLe data processing
def categorisealeksLeData(aleksLeString) -> dict:
    # Break into different lines
    aleksLeList = aleksLeString.split("\n")
    aleksLeHeader = aleksLeList.pop(firstEntry).split(",")
    # print(aleksLeHeader)
    aleksLeDictedList = []
    for aleksLeLine in aleksLeList:
        aleksLeLineList = aleksLeLine.split(",")
        aleksLeLineDict = createAleksLeDict(aleksLeHeader, aleksLeLineList)
        aleksLeDictedList.append(aleksLeLineDict)
    return {"list": aleksLeDictedList, "header": aleksLeHeader}

def createAleksLeDict(header, list):
    dictIterator = 0
    aleksLeLineDict = {}
    for aleksLeCategory in list:
        aleksLeLineDict[header[dictIterator]] = aleksLeCategory
        dictIterator += 1
    return aleksLeLineDict

def regexSearch(aleksLeData, searchTerm) -> list:
    searchResults = []

# Searching and Filtering Functions

# Display Functions
def aleksLeTable(aleksLeData, aleksLeHeader):
    table.setRowCount(len(aleksLeData))
    table.setColumnCount(len(aleksLeHeader))
    table.setHorizontalHeaderLabels(aleksLeHeader)
    for column in range(len(aleksLeHeader)):
        for row in range(len(aleksLeData)):
            table.setItem(row, column, QTableWidgetItem(aleksLeData[row][aleksLeHeader[column]]))

def main():
    aleksLeCSVString : str = open("aleksLe.csv").read()
    aleksLeData = categorisealeksLeData(aleksLeCSVString)
    #result = aleksLeSearch(aleksLeData, "Luke")
    aleksLeTable(aleksLeData["list"], aleksLeData["header"])

if __name__ == "__main__":
    main()
   

window.show()
