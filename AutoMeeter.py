import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QAction, QMenu, QPushButton, QLineEdit, \
    QHeaderView, QDateEdit, QTimeEdit
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QIcon
from pandas import DataFrame
from StorageSystem import DataBase
from threading import Thread
from plyer import notification
from time import sleep, time
from datetime import datetime, timedelta
from urllib.request import urlopen
import re
from enum import Enum

from MainWinUI4 import Ui_MainWindow
from AutoZoom import start_zoom_meeting
from AutoFCC import start_fcc_meeting
from AutoDiscord import start_discord_meeting
from RowModel import RowModel

# Get current Username
from os import getlogin
username = getlogin()

# Set app taskbar icon
# https://stackoverflow.com/a/1552105/984421 for more info
import ctypes
my_app_id = u'123'  # Custom application id
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)


def startMeeting(meetings_list, index):

    platform = str(meetings_list['Platform'][index])
    my_name = meetings_list['Name'][index]
    conf_id = meetings_list['ID'][index]
    conf_pass = meetings_list['Password'][index]

    # Notification alert
    notification.notify(title="AutoMeeter", message="Meeting has started!", app_name="AutoMeeter",
                        app_icon="./icons/logo.ico")

    if platform == 'Zoom':
        start_zoom_meeting(
            my_name=my_name,
            conference_id=conf_id,
            conference_pass=conf_pass,
            username=username
        )
        print('zoom meeting started')
    elif platform == 'FCC':
        start_fcc_meeting(
            my_name=my_name,
            conference_id=conf_id,
            conference_pass=conf_pass,
            username=username
        )
        print('fcc meeting started')
    elif platform == 'Discord':
        start_discord_meeting(
            my_name=my_name,
            conference_id=conf_id,
            conference_pass=conf_pass,
            username=username
        )
        print('discord meeting started')
    else:
        print('undefined platform')


def isNetworkConnected():
    is_connected = False
    time_for_connection = 10
    timeout = time() + time_for_connection
    while (not is_connected) and timeout > time():
        try:
            urlopen('http://google.com')
            is_connected = True
        except:
            is_connected = False
        sleep(1)
    return is_connected


class AutoMeeter(QMainWindow):

    class Column(Enum):
        MY_NAME = 0
        ID = 1
        PASS = 2
        DATE = 3
        TIME = 4
        ITERANCE = 5
        PLATFORM = 6

    row_model_object = RowModel()
    print("-sdjihuuwj: ", row_model_object.readRowModel().split('~@~'))

    close_buttons_list = []
    meetings_data = []
    cur_meetings_count = 0
    elements = []
    cols = ['Text', 'Text', 'Text', 'Date', 'Time', 'Text', 'Text']
    num_of_cols = cols.__len__()

    sql = DataBase()

    meeting_thread = None
    timer_thread = None
    timer_on_flag = None

    dragPos = None

    def __init__(self):
        super(AutoMeeter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.restoreData()

        self.startThread()

        # Adding Functions to Buttons
        self.ui.pushButton_close.clicked.connect(self.hide)
        self.ui.pushButton_hide.clicked.connect(self.hide)
        self.ui.pushButton_close.setToolTip("Close")
        self.ui.pushButton_hide.setToolTip("Minimize")
        self.ui.pushButton_add.clicked.connect(self.addMeeting)
        self.ui.pushButton_save.clicked.connect(self.saveTable)
        self.ui.pushButton_set.clicked.connect(self.setModel)

        self.setWindowIcon(QIcon('./icons/logo.png'))
        self.setWindowTitle("Icon")

        # Setting Up the Tray Menu
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./icons/logo.png"))
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.closeEvent)
        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        if not self.tray_icon.isVisible():
            self.tray_icon.show()
        self.show()

        self.tray_icon.activated.connect(self.systemIcon)
    def systemIcon(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def hideEvent(self, event):
        self.hide()
        event.accept()

    def closeEvent(self, event):
        self.tray_icon.hide()
        self.close()
        self.timer_on_flag = False
        print('Приложение успешно завершило работу')
        sys.exit()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def setModel(self):

        self.saveTable()

        i = self.cur_meetings_count-1
        RowModel.writeRowModel(
            self.row_model_object,
            self.meetings_data[i][self.Column.MY_NAME.value].text(),
            self.meetings_data[i][self.Column.ID.value].text(),
            self.meetings_data[i][self.Column.PASS.value].text(),
            self.meetings_data[i][self.Column.DATE.value].text(),
            self.meetings_data[i][self.Column.TIME.value].text(),
            self.meetings_data[i][self.Column.ITERANCE.value].text(),
            self.meetings_data[i][self.Column.PLATFORM.value].text(),
        )

    def addMeeting(self):

        model = RowModel.readRowModel(self.row_model_object).split('~@~')

        name = QLineEdit(self)
        conf_id = QLineEdit(self)
        conf_pass = QLineEdit(self)
        date = QDateEdit(self)
        time = QTimeEdit(self)
        iterance = QLineEdit(self)
        platform = QLineEdit(self)
        close = QPushButton(self)

        name.setText(model[self.Column.MY_NAME.value])
        conf_id.setText(model[self.Column.ID.value])
        conf_pass.setText(model[self.Column.PASS.value])
        iterance.setText(model[self.Column.ITERANCE.value])
        platform.setText(model[self.Column.PLATFORM.value])

        date.setDisplayFormat('dd.MM.yy')
        date.setDate(QDate().fromString(model[self.Column.DATE.value], 'dd.MM.yy'))

        time.setDisplayFormat('hh:mm')
        hours = int(re.search(r'[0-9]{1,2}', model[self.Column.TIME.value]).group())
        minutes = int(model[self.Column.TIME.value][-2] + model[self.Column.TIME.value][-1])
        time.setTime(QTime(hours, minutes))

        close.setIcon(QIcon('./icons/close-button.png'))
        close.setFlat(True)

        self.ui.tableWidget_table.insertRow(self.cur_meetings_count)
        close.setObjectName(str(self.cur_meetings_count))
        close.released.connect(lambda: self.deleteMeeting(close.objectName()))
        self.close_buttons_list.append(close)
        self.elements = [name, conf_id, conf_pass, date, time, iterance, platform, close]
        col = 0
        for element in self.elements:
            self.ui.tableWidget_table.setCellWidget(self.cur_meetings_count, col, element)
            col += 1

        header = self.ui.tableWidget_table.horizontalHeader()
        header.setSectionResizeMode(self.num_of_cols, QHeaderView.ResizeToContents)

        self.elements.remove(close)
        row = []
        for element, name in zip(self.elements, self.cols):
            element.setObjectName(name)
            row.append(element)
        self.meetings_data.append(row)
        self.cur_meetings_count += 1
        self.ui.tableWidget_table.scrollToBottom()

    def deleteMeeting(self, button_id):
        # get scroll position
        cur_scroll_pos = self.ui.tableWidget_table.verticalScrollBar().value()
        print(cur_scroll_pos)
        self.ui.tableWidget_table.removeRow(int(button_id))
        self.cur_meetings_count -= 1
        self.close_buttons_list.remove(self.close_buttons_list[int(button_id)])
        for i in range(self.cur_meetings_count):
            self.close_buttons_list[i].setObjectName(str(i))
        self.meetings_data.remove(self.meetings_data[int(button_id)])
        # set back scroll position
        self.ui.tableWidget_table.verticalScrollBar().setValue(cur_scroll_pos)

    def checkTable(self):
        i = 0
        while i < self.cur_meetings_count:
            date_i = self.meetings_data[i][self.Column.DATE.value].text()
            time_i = self.meetings_data[i][self.Column.TIME.value].text()
            iter_i = self.meetings_data[i][self.Column.ITERANCE.value].text()
            date_time = date_i + ' ' + time_i
            table_date = datetime.strptime(date_time, '%d.%m.%y %H:%M')
            today_date = datetime.today()
            if table_date < today_date:
                if iter_i == '':
                    self.deleteMeeting(i)
                    i -= 1
                else:
                    while table_date < today_date:
                        self.meetings_data[i][3].setDate(
                            QDate().fromString(self.meetings_data[i][self.Column.DATE.value].text(), 'dd.MM.yy').toPyDate() +
                            timedelta(int(iter_i))
                        )
                        date_time = self.meetings_data[i][3].text() + ' ' + time_i
                        table_date = datetime.strptime(date_time, '%d.%m.%y %H:%M')
            i += 1

    def saveTable(self):
        self.checkTable()
        data = []
        rows = []
        for x in range(len(self.meetings_data)):
            for i in range(self.num_of_cols):
                if self.meetings_data[x][i].objectName() == "Text":
                    data.append(self.meetings_data[x][i].text())
                elif self.meetings_data[x][i].objectName() == "Date":
                    data.append(self.meetings_data[x][i].text())
                elif self.meetings_data[x][i].objectName() == "Time":
                    data.append(self.meetings_data[x][i].text())
            rows.append(data)
            data = []
        meetings_data = DataFrame(rows, columns=('Name', 'ID', 'Password', 'Date', 'Time', 'Iterance', 'Platform'))
        self.sql.enterData(meetings_data)
        print('Saved table:')
        print(self.sql.readData())
        self.startThread()

    def restoreData(self):
        data = self.sql.readData()
        for x in range(len(data)):
            self.addMeeting()
            for y in range(len(data.columns)):
                if self.meetings_data[x][y].objectName() == "Text":
                    self.meetings_data[x][y].setText(data.loc[x][y])
                if self.meetings_data[x][y].objectName() == "Date":
                    date_y = QDate().fromString(data.loc[x][y], 'dd.MM.yy')
                    self.meetings_data[x][y].setDate(date_y)
                if self.meetings_data[x][y].objectName() == "Time":
                    time_y = QTime().fromString(data.loc[x][y], 'hh:mm')
                    self.meetings_data[x][y].setTime(time_y)
        self.ui.tableWidget_table.scrollToTop()

    def startThread(self):
        meetings_list = self.sql.readData()
        self.timer_on_flag = False
        self.timer_thread = Thread(target=self.timer, args=(meetings_list,))
        sleep(1)
        self.timer_thread.start()
        print('timer thread started')

    def timer(self, meetings_list):
        self.timer_on_flag = True
        while self.timer_on_flag:
            cur_date = str(datetime.now().strftime('%d.%m.%y'))
            cur_time = str(datetime.now().strftime('%H:%M:%S'))
            print("Time: ", cur_time)
            for i in range(len(meetings_list)):
                if (cur_date == meetings_list['Date'][i] and
                        cur_time == (meetings_list['Time'][i] + ':00')):
                    if isNetworkConnected():
                        self.meeting_thread = Thread(target=startMeeting, args=(meetings_list, i))
                        self.meeting_thread.start()
                        print('meeting thread started')
                        Thread(target=self.saveTable).start()
            sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = AutoMeeter()
    sys.exit(app.exec_())
