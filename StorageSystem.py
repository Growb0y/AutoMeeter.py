import sqlite3
from pandas import DataFrame

connection = sqlite3.connect('./data.db', check_same_thread=False)


class DataBase:
    cursor = connection.cursor()

    def __init__(self):
        self.createTable()

    def createTable(self):
        connection.execute(
            """CREATE TABLE IF NOT EXISTS MeetingsData 
            (Name text, ID text, Password text, Date text, Time text, Iterance text, Platform text)""")

    def enterData(self, meetings_data):
        meetings_data.to_sql('MeetingsData', con=connection, if_exists='replace', index=False)

    def readData(self):
        self.cursor.execute('''SELECT * FROM MeetingsData''')
        return DataFrame(self.cursor.fetchall(), columns=['Name', 'ID', 'Password', 'Date', 'Time', 'Iterance', 'Platform'])
