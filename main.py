import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

firstEntry = 0

# Creating the Window
app = QApplication([])

window = QWidget()
window.setObjectName("mainWindow")

# Create the layout and main table widget
gridLayout = QGridLayout()
table = QTableWidget()
searchEntry = QLineEdit()
searchButton = QPushButton("Search")
filterDropdown = QComboBox()

characterImage = QPixmap("aleksLe.png")
seriesImage = QPixmap("series.png")


# Create the image labels and set the images
characterImageLabel = QLabel()
characterImageLabel.setText("AleksLe Coming Soon...")
# characterImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# characterImageLabel.setPixmap(characterImage)
# characterImageLabel.setObjectName("characterImageLabel")
seriesImageLabel = QLabel()
seriesImageLabel.setText("Series Coming Soon...")
# seriesImageLabel.setPixmap(seriesImage)
# seriesImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
# seriesImageLabel.setObjectName("seriesImageLabel")

# align the widgets in the grid layout and add them to the window
window.setLayout(gridLayout)
gridLayout.addWidget(characterImageLabel, 0, 0)
gridLayout.addWidget(seriesImageLabel, 0, 1)
gridLayout.addWidget(searchEntry, 1, 0)
gridLayout.addWidget(searchButton, 1, 1)
gridLayout.addWidget(filterDropdown, 1, 2)
gridLayout.addWidget(table, 2, 0, 1, 3)

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
    # Load application stylesheet if present
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except Exception:
        pass

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

