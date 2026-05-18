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

def cleanUpFindall(unsanitised : list) :
    sanitised = []
    for entry in unsanitised:
        cleaningUp = "" 
        for text in entry:
            cleaningUp += text
        sanitised.append(cleaningUp)
    return sanitised


def refresh(searchTerm, filterList):
    # ^(?:(.*)$) Returns only the first line
    aleksLeHeader = getAleksLeHeader(aleksLeCSVString)
    aleksLeListicle = grandAleksLeFilter(aleksLeCSVString,searchTerm,filterList)
    aleksLeTable(aleksLeListicle, aleksLeHeader)

def getAleksLeHeader(CSVstring) -> list:
    header = [col.strip() for col in CSVstring.split("\n").pop(firstEntry).split(",")]
    return header
    # headerString = aleksLeCSVString.split("\n").pop(firstEntry)
    # headerList = headerString.split(",")
    # for headerEntry in headerList:
    #     headerEntry.strip()
    # aleksLeHeader = headerList

def grandAleksLeFilter(aleksLeCSVString,searchTerm,filterList):
    disgustingRegex = searchFilterRegexConstructor(searchEntry.text(), filterList)
    unsanitised = findall(disgustingRegex, aleksLeCSVString, MULTILINE)
    sanitised = cleanUpFindall(unsanitised)
    splitUp = []
    for unsplit in sanitised:
        nowSplit = unsplit.split(",")
        for word in nowSplit:
            word.strip()
        splitUp.append(nowSplit)
    return splitUp

def viewAllInCategory(category) -> list:
    categoryNumber = aleksLeHeader.index(category) - firstEntry
    simpleRegex = r"^(?<=\n)((?=([^,]*,){" + str(categoryNumber) + r"}))"
    justThat = cleanUpFindall(findall(simpleRegex, aleksLeCSVString, MULTILINE))
    print(justThat)

# Display Functions
def aleksLeTable(aleksLeList, aleksLeHeader):
    tableList = aleksLeList
    tableheader = aleksLeHeader
    table.clear()
    print(tableList)
    table.setRowCount(len(tableList))
    table.setColumnCount(len(tableheader))
    table.setHorizontalHeaderLabels(tableheader)

    for row in range(len(tableList)):
        for column in range(len(tableheader)):
            table.setItem(row, column, QTableWidgetItem(tableList[row][column]))
    

def searchFilterRegexConstructor(searchText, filterList) -> str:
    # Search Text Regex: ^(.*)(\bSEARCHTEXT\b)(.*)
    # Filter Text Regex: ^([^,]*,){FILTERNUMBER}\s*(\bFILTERTEXT\b)(.*)
    # Put them together with positive lookaheads and get
    # ^(?<=\n)(?=([^,]*,){FILTERNUMBER}\s*(\bFILTERTEXT\b)(.*))(?=(.*)(\bSEARCHTEXT\b)(.*)).*$
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

# Filter Mechanics holy molyyy this was a pain
def populateDropdown(dropdown, addList:list):
    for entry in addList :
        dropdown.addItem(entry)

def createFilters():
    pass

# def aleksLeFilterCategoryUpdate(aleksLeData):
#     filterEntry.clear()
#     category = filterCategory.currentText()
#     if category == "None":
#         pass
#     for entry in aleksLeData["list"]:
#         if entry.get(category, "") not in [filterEntry.itemText(i) for i in range(filterEntry.count())]:
#             filterEntry.addItem(entry.get(category, ""))


# Relevant Variables
firstEntry = 0
filterList = []

aleksLeCSVString : str = open("aleksLe.csv").read() # The Raw CSV String
aleksLeHeader = getAleksLeHeader(aleksLeCSVString)
aleksLeList = []


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

filterDropdown = QComboBox()
filterEntry = QComboBox()
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
# GO FOR SIMPLE FILTER
searchnfilterGrid = QGridLayout()
#filterGrid = QGridLayout()
searchnfilterGrid.addWidget(searchEntry, 0, 0)
searchnfilterGrid.addWidget(searchButton, 0, 1)
#searchnfilterGrid.addWidget(filterText, 1, 0)
#searchnfilterGrid.addWidget(filterAddButton, 1, 1)
#searchnfilterGrid.addLayout(filterGrid, 2, 0, 1, 2)
searchnfilterGrid.addWidget(filterDropdown, 1, 0)
searchnfilterGrid.addWidget(filterEntry, 1, 1)


# init and connect search n filter buttons
filterAddButton.clicked.connect(createFilters)
populateDropdown(filterDropdown, aleksLeHeader)
filterDropdown.currentIndexChanged.connect(lambda: viewAllInCategory(filterDropdown.currentText()))

searchButton.clicked.connect(lambda: refresh(searchEntry.text(),filterList))
#filterCategory.currentIndexChanged.connect(lambda:aleksLeFilterCategoryUpdate(aleksLeData))

# align the widgets in the grid layout and add them to the window
window.setLayout(gridLayout)
gridLayout.addWidget(characterImageLabel, 0, 0)
gridLayout.addWidget(seriesImageLabel, 0, 1)
gridLayout.addLayout(searchnfilterGrid, 2, 0, 1, 4)
gridLayout.addWidget(table, 3, 0, 1, 4)


if __name__ == "__main__":
    main()

