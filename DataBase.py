import time
import math
import sqlite3

class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        sql = 'SELECT * FROM users'
        try:
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return result
        
        except:
            print('Помилка читтаня БД')
        
        return []

    
    def addAccount(self, name, password):
        try: 
            # tm = math.floor(time.time())
            self.__cursor.execute('INSERT INTO users VALUES (NULL, ?, ?, ?)', (name, password, 0))
            self.__db.commit()
        
        except sqlite3.Error as e:
            print('Помилка додавання статті в БВ', e)
            return False

        return True

    def getAccount(self):
        try: 
            self.__cursor.execute('SELECT name, password FROM posts WHERE name="andrew17" LIMIT 1')
            result = self.__cursor.fetchall()
            if result:
                return result

        except sqlite3.Error as e:
            print('Помилка читання статті із БВ', e)
            return False

        return (False, False)