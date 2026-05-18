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
from re import (
    split,
    findall, 
    sub,
    MULTILINE
)


# Relevant Variables
firstEntry = 0
aleksLeData = []
filterList = [
    {
        "category": "Role Scale",
        "entry": "Lead",
    },
    {
        "category": "Medium",
        "entry": "Video Game",
    }
]

aleksLeCSVString : str = open("aleksLe.csv").read() # The Raw CSV String
aleksLeHeader = getAleksLeHeader(aleksLeCSVString)

def refresh():
    # ^(?:(.*)$) Returns only the first line
    aleksLeHeader = getAleksLeHeader(aleksLeCSVString)
    aleksLeListicle = grandAleksLeFilter(aleksLeCSVString)

def getAleksLeHeader(CSVstring) -> list:
    header = [col.strip() for col in CSVstring.split("\n").pop(firstEntry).split(",")]
    return header
    # headerString = aleksLeCSVString.split("\n").pop(firstEntry)
    # headerList = headerString.split(",")
    # for headerEntry in headerList:
    #     headerEntry.strip()
    # aleksLeHeader = headerList

def grandAleksLeFilter():
    disgustingRegex = searchFilterRegexConstructor(searchEntry.text(), filterList)
    print(disgustingRegex)
    unsanitised = findall(disgustingRegex, aleksLeCSVString, MULTILINE)
    print(unsanitised)
    # for entry in unsanitised: 
    #     sub()

# Functions for AleksLe data processing
def categorisealeksLeData(aleksLeString) -> dict:
    # Break into different lines
    aleksLeList = aleksLeString.split("\n")
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

# Display Functions
def aleksLeTable(aleksLeData):
    tableList = aleksLeData["list"]
    tableheader = aleksLeData["header"]
    table.clear()
    table.setRowCount(len(tableList))
    table.setColumnCount(len(tableheader))
    table.setHorizontalHeaderLabels(tableheader)

    # check the row for the conditions, when met add to table
    for row in range(len(tableList)):
        # Filtering
        # if not checkFilters(tableList[row], filterCategory.currentText(), filterEntry.currentText()):
        #     continue
        # Searching with a regex search function
        # if not regexSearch(tableList[row], searchEntry.text()):
        #     continue

        for column in range(len(tableheader)):
            table.setItem(row, column, QTableWidgetItem(tableList[row].get(tableheader[column], "")))
    

def searchFilterRegexConstructor(searchText, filterList) -> str:
    # Search Text Regex: ^(.*)(\bSEARCHTEXT\b)(.*)
    # Filter Text Regex: ^([^,]*,){FILTERNUMBER}\s*(\bFILTERTEXT\b)(.*)
    # Put them together with positive lookaheads and get
    # ^(?=([^,]*,){FILTERNUMBER}\s*(\bFILTERTEXT\b)(.*))(?=(.*)(\bSEARCHTEXT\b)(.*)).*$
    # Since I use positive lookaheads they are repeatable :)
    gigaRegex = r"^(?<=\n)" # start and skip first line (header)
    # start with search text positive lookahead
    gigaRegex += r"(?=(.*)(\b" + searchText + r"\b)(.*))"
    # add the filters with positive lookaheads
    for filter in filterList:
        # Take it line by line so I can read it (╥.╥) 
        gigaRegex += r"(?=([^,]*,){"
        gigaRegex += str(aleksLeHeader.index(filter["category"]))
        gigaRegex += r"}\s*(\b" 
        gigaRegex += filter["entry"] 
        gigaRegex += r"\b)(.*))"
    gigaRegex += r".*$" # End of line
    return gigaRegex

def regexSnipper(regex, fullString, ) -> list:
    matches = findall(regex, fullString, MULTILINE)
    return matches

# Filter Mechanics holy molyyy this was a pain
def checkFilters(checkDictionary, category, entry) -> bool:
    if category == "None":
        return True
    if checkDictionary.get(category, "") == entry:
        return True
    return False

def checkAvailableFilterCategories():
    occupiedCategories = []
    for filter in filterList:
        occupiedCategories.append(filter["category"].currentText())
    availableCategories = []
    for category in aleksLeData["header"]:
        if category not in occupiedCategories:
            availableCategories.append(category)
    return availableCategories
    #return aleksLeData["header"]

#filterList = []
def createFilters(): 

    pass

def deleteFilters(filterIndex): 
    pass

def filterCategoryUpdate(filterCategorySelection,filterListIndex):
    pass
def filterEntryUpdate(filterEntrySelection,filterListIndex):
    pass
def filterListUpdate():
    pass

def filterGridUpdate():
    for filter in filterList:
        filterGrid.addWidget(filter["category"], filterList.index(filter), 0)
        filterGrid.addWidget(filter["entry"], filterList.index(filter), 1)
        filterGrid.addWidget(filter["deleteButton"], filterList.index(filter), 2)


# def aleksLeFilterCategoryUpdate(aleksLeData):
#     filterEntry.clear()
#     category = filterCategory.currentText()
#     if category == "None":
#         pass
#     for entry in aleksLeData["list"]:
#         if entry.get(category, "") not in [filterEntry.itemText(i) for i in range(filterEntry.count())]:
#             filterEntry.addItem(entry.get(category, ""))

def main():
    #aleksLeTable(aleksLeData)

    print(searchFilterRegexConstructor("Luke", filterList))
    window.show()
    sys.exit(app.exec())


# Creating the Window
app = QApplication([])
app.setStyleSheet(open("style.qss", "r").read())

window = QWidget()
window.setObjectName("mainWindow")

# Create the main table widget
gridLayout = QGridLayout()
table = QTableWidget()

searchEntry = QLineEdit()
searchButton = QPushButton("Search")

filterText = QLabel("Filters")
filterAddButton = QPushButton("Add Filter")

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

# Search and filter layout
searchnfilterGrid = QGridLayout()
filterGrid = QGridLayout()
searchnfilterGrid.addWidget(searchEntry, 0, 0)
searchnfilterGrid.addWidget(searchButton, 0, 1)
searchnfilterGrid.addWidget(filterText, 1, 0)
searchnfilterGrid.addWidget(filterAddButton, 1, 1)
searchnfilterGrid.addLayout(filterGrid, 2, 0, 1, 2)

# init and connect search n filter buttons
filterAddButton.clicked.connect(createFilters)

searchButton.clicked.connect(lambda: refresh())
#filterCategory.currentIndexChanged.connect(lambda:aleksLeFilterCategoryUpdate(aleksLeData))

# align the widgets in the grid layout and add them to the window
window.setLayout(gridLayout)
gridLayout.addWidget(characterImageLabel, 0, 0)
gridLayout.addWidget(seriesImageLabel, 0, 1)
gridLayout.addLayout(searchnfilterGrid, 2, 0, 1, 4)
gridLayout.addWidget(table, 3, 0, 1, 4)


if __name__ == "__main__":
    main()

