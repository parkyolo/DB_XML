import pymysql
import sys, datetime, csv, json
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:     # dictionary based cursor
                cursor.execute(sql, params)
                tuples = cursor.fetchall()
                return tuples
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:
    # 모든 검색문은 여기에 각각 하나의 메소드로 정의
    def selectPlayerTeam(self):
        sql = "SELECT DISTINCT team_name FROM team"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerPosition(self):
        sql = "SELECT DISTINCT position FROM player"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayerNation(self):
        sql = "SELECT DISTINCT nation FROM player"
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectTeamId(self, value):
        sql = "SELECT team_id FROM team WHERE team_name = %s"
        params = (value)

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

    def selectPlayer(self, txt):
        sql = txt
        params = ()

        util = DB_Utils()
        tuples = util.queryExecutor(db="kleague", sql=sql, params=params)
        return tuples

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        # 윈도우 설정
        self.setWindowTitle("선수 테이블 검색 & 파일 출력")

        # 위젯 설정
        self.label1 = QLabel("팀명: ")
        self.combo1 = QComboBox(self)
        self.label2 = QLabel("포지션: ")
        self.combo2 = QComboBox(self)
        self.label3 = QLabel("출신국: ")
        self.combo3 = QComboBox(self)

        self.label4 = QLabel("키: ")
        self.lineEdit1 = QLineEdit()
        self.lineEdit1.setValidator(QIntValidator(self))
        self.radio1 = QRadioButton("이상")
        self.radio1.setChecked(True)
        self.radio2 = QRadioButton("이하")

        self.label5 = QLabel("몸무게: ")
        self.lineEdit2 = QLineEdit()
        self.lineEdit2.setValidator(QIntValidator(self))
        self.radio3 = QRadioButton("이상")
        self.radio3.setChecked(True)
        self.radio4 = QRadioButton("이하")

        self.clearButton= QPushButton("초기화")
        self.clearButton.clicked.connect(self.clearButton_Clicked)
        self.searchButton = QPushButton("검색")
        self.searchButton.clicked.connect(self.searchButton_Clicked)

        self.resultTable = QTableWidget(self)

        self.radio5 = QRadioButton("CSV")
        self.radio5.setChecked(True)
        self.radio6 = QRadioButton("JSON")
        self.radio7 = QRadioButton("XML")
        self.saveButton = QPushButton("저장")
        self.saveButton.clicked.connect(self.saveButton_Clicked)

        # 레이아웃의 생성, 위젯 연결, 레이아웃 설정
        layout = QVBoxLayout()

        searchBox = QGroupBox("선수 검색")

        teamLayout = QHBoxLayout()
        teamLayout.addWidget(self.label1)
        teamLayout.addWidget(self.combo1)

        positionLayout = QHBoxLayout()
        positionLayout.addWidget(self.label2)
        positionLayout.addWidget(self.combo2)

        nationLayout = QHBoxLayout()
        nationLayout.addWidget(self.label3)
        nationLayout.addWidget(self.combo3)

        heightLayout = QHBoxLayout()
        heightLayout.addWidget(self.label4)
        heightLayout.addWidget(self.lineEdit1)
        heightButton = QButtonGroup(self)
        heightButton.addButton(self.radio1)
        heightButton.addButton(self.radio2)
        heightLayout.addWidget(self.radio1)
        heightLayout.addWidget(self.radio2)

        weightLayout = QHBoxLayout()
        weightLayout.addWidget(self.label5)
        weightLayout.addWidget(self.lineEdit2)
        weightButton = QButtonGroup(self)
        weightButton.addButton(self.radio3)
        weightButton.addButton(self.radio4)
        weightLayout.addWidget(self.radio3)
        weightLayout.addWidget(self.radio4)

        comboLayout = QHBoxLayout()
        comboLayout.addLayout(teamLayout)
        comboLayout.addStretch(1)
        comboLayout.addLayout(positionLayout)
        comboLayout.addStretch(1)
        comboLayout.addLayout(nationLayout)

        editLayout = QHBoxLayout()
        editLayout.addLayout(heightLayout)
        editLayout.addStretch(1)
        editLayout.addLayout(weightLayout)

        optionLayout = QVBoxLayout()
        optionLayout.addLayout(comboLayout)
        optionLayout.addLayout(editLayout)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.searchButton)

        searchLayout = QHBoxLayout()
        searchLayout.addSpacing(50)
        searchLayout.addLayout(optionLayout)
        searchLayout.addSpacing(50)
        searchLayout.addLayout(buttonLayout)

        searchBox.setLayout(searchLayout)

        outputBox = QGroupBox("파일 출력")

        typeLayout = QHBoxLayout()
        typeLayout.addWidget(self.radio5)
        typeLayout.addStretch(1)
        typeLayout.addWidget(self.radio6)
        typeLayout.addStretch(1)
        typeLayout.addWidget(self.radio7)

        outputLayout = QHBoxLayout()
        outputLayout.addSpacing(50)
        outputLayout.addLayout(typeLayout)
        outputLayout.addSpacing(250)
        outputLayout.addWidget(self.saveButton)

        outputBox.setLayout(outputLayout)

        layout.addWidget(searchBox)
        layout.addWidget(self.resultTable)
        layout.addWidget(outputBox)
        self.setLayout(layout)

        # DB 검색문 실행
        query = DB_Queries()
        teams = query.selectPlayerTeam()
        positions = query.selectPlayerPosition()
        nations = query.selectPlayerNation()

        team_columnName = list(teams[0].keys())[0]
        self.team_items = [team[team_columnName] for team in teams]
        self.combo1.addItem('ALL')
        self.combo1.addItems(self.team_items)
        self.combo1.setCurrentIndex(0)

        position_columnName = list(positions[0].keys())[0]
        self.position_items = ['미정' if position[position_columnName] == None else position[position_columnName] for position in positions]
        self.combo2.addItem('ALL')
        self.combo2.addItems(self.position_items)
        self.combo2.setCurrentIndex(0)

        nation_columnName = list(nations[0].keys())[0]
        self.nation_items = ['대한민국' if nation[nation_columnName] == None else nation[nation_columnName] for nation in nations]
        self.combo3.addItem('ALL')
        self.combo3.addItems(self.nation_items)
        self.combo3.setCurrentIndex(0)

    def clearButton_Clicked(self):
        self.combo1.setCurrentIndex(0)
        self.combo2.setCurrentIndex(0)
        self.combo3.setCurrentIndex(0)
        self.lineEdit1.clear()
        self.lineEdit2.clear()
        self.radio1.setChecked(True)
        self.radio3.setChecked(True)
        self.radio5.setChecked(True)
        self.resultTable.clearContents()

    def searchButton_Clicked(self):
        team = self.combo1.currentText()
        position = self.combo2.currentText()
        nation = self.combo3.currentText()
        height = self.lineEdit1.text()
        weight = self.lineEdit2.text()
        
        sql = "SELECT * FROM player"

        where = []
        # DB 검색문 실행
        query = DB_Queries()
        if team != 'ALL':
            team_dic = query.selectTeamId(team)
            team_id = list(team_dic[0].values())[0]
            where.append("team_id = '" + team_id + "'")
        if position != 'ALL':
            where.append("position IS NULL" if position == "미정" else ("position = '" + position + "'"))
        if nation != 'ALL':
            where.append("nation IS NULL" if nation == "대한민국" else ("nation = '" + nation + "'"))

        if height:
            comp = " >= " if self.radio1.isChecked() else " <= "
            where.append("height" + comp + height)
        if weight:
            comp = " >= " if self.radio3.isChecked() else " <= "
            where.append("weight" + comp + weight)

        if where:
            sql += " WHERE " + " AND ".join(where)

        self.players = query.selectPlayer(sql)

        if self.players is None:
            return

        self.resultTable.clearContents()
        self.resultTable.setRowCount(len(self.players))
        self.resultTable.setColumnCount(len(self.players[0]))
        columnNames = list(self.players[0].keys())
        self.resultTable.setHorizontalHeaderLabels(columnNames)
        self.resultTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for player in self.players:
            rowIDX = self.players.index(player)

            for k, v in player.items():
                columnIDX = list(player.keys()).index(k)

                if k == 'POSITION' and v is None:
                    self.players[rowIDX]['POSITION'] = '미정'
                    item = QTableWidgetItem('미정')
                elif k == 'NATION' and v is None:
                    self.players[rowIDX]['NATION'] = '대한민국'
                    item = QTableWidgetItem('대한민국')
                elif v == None:
                    continue
                elif isinstance(v, datetime.date):
                    self.players[rowIDX]['BIRTH_DATE'] = v.strftime('%Y-%m-%d')
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                self.resultTable.setItem(rowIDX, columnIDX, item)

        self.resultTable.resizeColumnsToContents()
        self.resultTable.resizeRowsToContents()

    def saveButton_Clicked(self):
        if self.players is None:
            return

        if self.radio5.isChecked():
            with open('players.csv', 'w', encoding='utf-8', newline='') as f:
                wr = csv.writer(f)
                columnNames = list(self.players[0].keys())
                # 테이블 컬럼명을 파일의 첫 줄에 기록
                wr.writerow(columnNames)
                for player in self.players:
                    row = list(player.values())
                    wr.writerow(row)

        elif self.radio6.isChecked():
            newDict = dict(players = self.players)
            with open('players.json', 'w', encoding='utf-8') as f:
                json.dump(newDict, f, indent=4, ensure_ascii=False)

        elif self.radio7.isChecked():
            newDict = dict(player = self.players)
            tableName = list(newDict.keys())[0]
            tableRows = list(newDict.values())[0]

            rootElement = ET.Element('TABLE')
            rootElement.attrib['name'] = tableName

            for row in tableRows:
                rowElement = ET.Element('ROW')
                rootElement.append(rowElement)

                # 각 속성 값은 ROW 엘리먼트의 attribute
                for columnName in list(row.keys()):
                    if row[columnName] == None:
                        rowElement.attrib[columnName] = ''
                    else:
                        rowElement.attrib[columnName] = row[columnName]

                    if type(row[columnName]) == int:
                        rowElement.attrib[columnName] = str(row[columnName])

            ET.ElementTree(rootElement).write('players.xml', encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()