from Web_Scraping import WebScraping
import sqlite3

from Web_Scraping import WebScraping
import sqlite3


class Database:
    def __init__(self, db_name, table_name):
        self.dataBase_name = db_name
        self.table_name = table_name
        self.web_scraped = WebScraping()

    def get_scraped_data(self):
        data = self.web_scraped.get_data()
        return data

    def connect(self):
        try:
            sqliteConnection = sqlite3.connect(self.dataBase_name)
            cursor = sqliteConnection.cursor()
            print("Database created and successfully connected to SQLite")
            sqlite_select_Query = "select sqlite_version();"
            cursor.execute(sqlite_select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
            cursor.close()

        except sqlite3.Error as error:
            print(f'Error while connecting to sqlite {error}')

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def createTable(self):
        try:
            sqliteConnection = sqlite3.connect(self.dataBase_name)

            sqlite_create_table_query = f'''CREATE TABLE IF NOT EXISTS {self.table_name}(year INTEGER, CO2 REAL, CH4 
            REAL, N2O REAL, CFC12 REAL, CFC11 REAL, minor REAL ) '''

            cursor = sqliteConnection.cursor()
            print("Successfully connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            print('SQLite table created')
            cursor.close()

        except sqlite3.Error as error:
            print('Error while creating as a sqlite table', error)

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print('sqlite connection is closed.')

    def insert(self):
        try:
            sqliteConnection = sqlite3.connect(self.dataBase_name)
            cursor = sqliteConnection.cursor()
            print('Connected to SQLite')

            data = self.get_scraped_data()
            for i in data:
                year = i[0]
                CO2 = i[1]
                CH4 = i[2]
                N2O = i[3]
                CFC12 = i[4]
                CFC11 = i[5]
                minor = i[6]
                sqlite_insert_query = f'''INSERT INTO {self.table_name}
                (year, CO2, CH4, N2O, CFC12, CFC11, minor) VALUES(?, ?, ?, ?, ?, ?, ?)'''

                data_tuple = (year, CO2, CH4, N2O, CFC12, CFC11, minor)
                cursor.execute(sqlite_insert_query, data_tuple)
            sqliteConnection.commit()
            print('File inserted successfully as into a table')
            cursor.close()

        except sqlite3.Error as error:
            print(f'Failed to insert data into sqlite table {error}')

        finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print(f'The sqlite connection is closed')

    def readTable(self):
        try:
            sqliteConnection = sqlite3.connect(self.dataBase_name)
            cursor = sqliteConnection.cursor()
            print('connected to SQLite')
            sqlite_select_query = f"SELECT * from {self.table_name}"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print(f'Total rows are: {len(records)}')

        except sqlite3.Error() as error:
            print(f'Failed to read data from sqlite table {error}')

        finally:
            sqliteConnection.close()
            print('The SQLite connection is closed')

    def fetch(self):
        con = sqlite3.connect(self.dataBase_name)
        cursorObj = con.cursor()
        sel = f"SELECT * from {self.table_name}"
        cursorObj.execute(sel)
        return cursorObj.fetchall()

    def temp(self, element, lock):
        con = sqlite3.connect(self.dataBase_name)
        cursorObj = con.cursor()
        lst = []
        for i in range(1979, 2021):
            with lock:
                sel = f"SELECT year, {element} from {self.table_name} WHERE year = ?"
                cursorObj.execute(sel, (i,))
                lst.append(cursorObj.fetchone())
                new_dict = {}
                for i in lst:
                    new_dict[i[0]] = i[1]

        return new_dict

#s = Database('SQLite_Python.db', 'Database')
#print(s.get_scraped_data())
#s.connect()
#s.createTable()
#s.insert()
# s.readTable()
#print(s.fetch())



