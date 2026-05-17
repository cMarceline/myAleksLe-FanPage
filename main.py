import sys
from PySide6.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QGridLayout,     
    QMessageBox, 
    QTableWidget, 
    QTableWidgetItem,
    QComboBox
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt

firstEntry = 0


# Functions for AleksLe data processing
def categorisealeksLeData(aleksLeString) -> dict:
    # Break into different lines
    aleksLeList = aleksLeString.split("\n")
    aleksLeHeader = [col.strip() for col in aleksLeList.pop(firstEntry).split(",")]
    # print(aleksLeHeader)
    aleksLeDictedList = []
    for aleksLeLine in aleksLeList:
        aleksLeLineList = [value.strip() for value in aleksLeLine.split(",")]
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

def regexSearch(checkDictionary, searchTerm) -> bool:
    for key in checkDictionary:
        if searchTerm in checkDictionary[key]:
            return True
    return False

# Display Functions
def aleksLeTable(aleksLeData, aleksLeHeader):
    table.clear()
    table.setRowCount(len(aleksLeData))
    table.setColumnCount(len(aleksLeHeader))
    table.setHorizontalHeaderLabels(aleksLeHeader)

    # check the row for the conditions, when met add to table
    for row in range(len(aleksLeData)):
        # Filtering
        if filterCategory.currentText() != "None" and filterEntry.currentText() != "":
            if aleksLeData[row].get(filterCategory.currentText(), "") != filterEntry.currentText(): 
                continue
        # Searching with a regex search function
        if not regexSearch(aleksLeData[row], searchEntry.text()):
            continue

        for column in range(len(aleksLeHeader)):
            table.setItem(row, column, QTableWidgetItem(aleksLeData[row].get(aleksLeHeader[column], "")))

def aleksLeFilterCategoryUpdate():
    filterEntry.clear()
    category = filterCategory.currentText()
    for row in range(table.rowCount()):
        item = table.item(row, filterCategory.currentIndex())
        if item and item.text() not in [filterEntry.itemText(i) for i in range(filterEntry.count())]:
            filterEntry.addItem(item.text())

aleksLeData : dict = {"list": [], "header": []}
def main():
    aleksLeCSVString : str = open("aleksLe.csv").read()
    aleksLeData = categorisealeksLeData(aleksLeCSVString)
    #result = aleksLeSearch(aleksLeData, "Luke")
    filterCategory.addItem("None")
    for category in aleksLeData["header"]:
        filterCategory.addItem(category)
    aleksLeTable(aleksLeData["list"], aleksLeData["header"])
    # Load application stylesheet if present

    window.show()
    sys.exit(app.exec())


# Creating the Window
app = QApplication([])
app.setStyleSheet(open("style.qss", "r").read())

window = QWidget()
window.setObjectName("mainWindow")

# Create the layout and main table widget
gridLayout = QGridLayout()
table = QTableWidget()

searchEntry = QLineEdit()
searchButton = QPushButton("Search")

filterCategory = QComboBox()
filterEntry = QComboBox()

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

# Bind the buttons to their functions
searchnfilterGrid = QGridLayout()
searchnfilterGrid.addWidget(searchEntry, 0, 0)
searchnfilterGrid.addWidget(searchButton, 0, 1)
searchnfilterGrid.addWidget(filterCategory, 1, 0)
searchnfilterGrid.addWidget(filterEntry, 1, 1)
searchButton.clicked.connect(lambda:aleksLeTable(aleksLeData["list"], aleksLeData["header"]))
filterCategory.currentIndexChanged.connect(aleksLeFilterCategoryUpdate)

# align the widgets in the grid layout and add them to the window
window.setLayout(gridLayout)
gridLayout.addWidget(characterImageLabel, 0, 0)
gridLayout.addWidget(seriesImageLabel, 0, 1)
gridLayout.addLayout(searchnfilterGrid, 2, 0, 1, 4)
gridLayout.addWidget(table, 3, 0, 1, 4)


if __name__ == "__main__":
    main()

