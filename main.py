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
    QComboBox,
    QSizePolicy
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
    print(disgustingRegex)
    unsanitised = findall(disgustingRegex, aleksLeCSVString, MULTILINE)
    print(unsanitised)
    sanitised = cleanUpFindall(unsanitised)
    splitUp = []
    for unsplit in sanitised:
        nowSplit = unsplit.split(",")
        for word in nowSplit:
            word.strip()
        splitUp.append(nowSplit)
    return splitUp

def viewAllInCategory(category) -> list:
    categoryNumber = aleksLeHeader.index(category)
    categoryNumber += 1 # skip the blank clause
    simpleRegex = r"^(?<=\n)((?=([^,]*,){" + str(categoryNumber) + r"}))"
    justThat = cleanUpFindall(findall(simpleRegex, aleksLeCSVString, MULTILINE))
    stripped = []
    for entry in justThat:
        stripped.append(entry.strip().strip(","))
    unduped = list(set(stripped))
    return unduped

# Display Functions
def aleksLeTable(aleksLeList, aleksLeHeader):
    tableList = aleksLeList
    tableheader = aleksLeHeader
    table.clear()
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
def populateDropdown(dropdown, addList:list, addBlank:bool=False):
    dropdown.clear()
    if addBlank:
        dropdown.addItem("")
    for entry in addList :
        dropdown.addItem(entry)

def refreshFilterList():
    filterList = [{
        "category" : filterDropdown.currentText(),
        "entry" : filterEntry.currentText()
    }]
    refresh(searchEntry.text(),filterList)


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
filterList = [{
    "category" : "Character",
    "entry" : "Luke"
}]

aleksLeCSVString : str = open("aleksLeTiny.csv").read() # The Raw CSV String
aleksLeHeader = getAleksLeHeader(aleksLeCSVString)
aleksLeList = []


def main():
    refresh(searchEntry.text(),filterList)
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())


# Creating the Window
app = QApplication([])
app.setStyleSheet(open("style.qss", "r").read())

window = QWidget()
window.setObjectName("mainWindow")

# Create the main table widget
gridLayout = QGridLayout()
gridLayout.setObjectName("finalGrid")
table = QTableWidget()

searchText = QLabel("Search Here!")
searchEntry = QLineEdit()
searchButton = QPushButton("Search")

filterText = QLabel("Filters!")
filterDropdown = QComboBox()
filterEntry = QComboBox()
filterAddButton = QPushButton("Add Filter")


# Create the image labels and set the images
characterImageLabel = QLabel()
characterImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
characterImageLabel.setPixmap(QPixmap("aleksLe.png"))
characterImageLabel.setScaledContents(True)
characterImageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
# characterImageLabel.setMaximumWidth(400)
characterImageLabel.setObjectName("aleksLeImage")

# Search and filter layout
searchnfilterGrid = QGridLayout()
searchnfilterGrid.setColumnStretch(0, 10)  # column 0 fills available space
searchnfilterGrid.setColumnStretch(1, 0)   # column 1 takes only its natural width
searchnfilterGrid.setColumnStretch(2, 7)   # column 2 gets a large share (~75%)
#filterGrid = QGridLayout()
searchnfilterGrid.addWidget(searchText, 0, 0)
searchnfilterGrid.addWidget(searchEntry, 0, 1)
searchnfilterGrid.addWidget(searchButton, 0, 2)
searchnfilterGrid.addWidget(filterText, 1, 0)
searchnfilterGrid.addWidget(filterDropdown, 1, 1)
searchnfilterGrid.addWidget(filterEntry, 1, 2)
searchnfilterGrid.setColumnStretch(0,1)
searchnfilterGrid.setColumnStretch(1,8)
searchnfilterGrid.setColumnStretch(2,1)

# init and connect search n filter buttons
populateDropdown(filterDropdown, aleksLeHeader)
populateDropdown(filterEntry,viewAllInCategory(filterDropdown.currentText()),True)

# filterDropdown.currentIndexChanged.connect(
#     lambda: populateDropdown(
#         filterEntry,viewAllInCategory(filterDropdown.currentText()),True
#     )
# )
# filterEntry.currentIndexChanged.connect(
#     lambda: refreshFilterList()
# )
# searchButton.clicked.connect(
#     lambda: refreshFilterList()
# )

#filterCategory.currentIndexChanged.connect(lambda:aleksLeFilterCategoryUpdate(aleksLeData))

# align the widgets in the grid layout and add them to the window
window.setLayout(gridLayout)
gridLayout.addWidget(characterImageLabel, 0, 0, 1, 4)
gridLayout.addLayout(searchnfilterGrid, 1, 0, 1, 4)
gridLayout.addWidget(table, 2, 0, 1, 4)
gridlayoutStretch = [2,1,4]
gridLayout.setRowStretch(0,2)
gridLayout.setRowStretch(1,1)
gridLayout.setRowStretch(2,4)



if __name__ == "__main__":
    main()

