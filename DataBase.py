from random import randint
from flask import flash
import time
import math
import sqlite3


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def showAccounts(self, find_user):
        try:
            self.__cursor.execute(f'SELECT name, password, dick FROM users \
                WHERE name = "{find_user}"')
            result = self.__cursor.fetchall()
            if result:
                return result
        
        except Exception as e:
            print('Помилка читтаня БД', e)
        
        return []

    def showallaccounts(self):
        try:
            self.__cursor.execute(f'SELECT name, dick FROM users ORDER BY dick DESC;')
            result = self.__cursor.fetchall()
            if result:
                return result

        except Exception as e:
            print('Помилка читання всіх гравців', e)


    def addAccount(self, name, password):
        try: 
            # tm = math.floor(time.time())
            self.__cursor.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?)', \
                (name, password, 0, 5))
            self.__db.commit()
        
        except sqlite3.Error as e:
            print('Помилка додавання акаунта в БВ', e)
            return False

        return True



    def singAccount(self, name, password):
        try:
            self.__cursor.execute(f'SELECT name, password FROM users WHERE name = "{name}" \
                AND password = "{password}";')
            if self.__cursor.fetchone() is None:
                return False

            else:
                return True
                # вхід був виконаний
        
        except Exception as e:
            print('Помилка входу', e)
        
        # return (False, False)

    def play(self, name):
        random_length = randint(-20, 20)
        try:
            for i in self.__cursor.execute(f"SELECT dick, countchoice FROM users \
                                                WHERE name = '{name}'"):
                balance = i['dick']
                update = i['countchoice'] 
                if i['countchoice'] < 0:
                    return False
                    
                
                else:
                    self.__cursor.execute(f'UPDATE users SET dick = {random_length + balance} WHERE name = "{name}"')
                    self.__cursor.execute(f'UPDATE users SET countchoice = {update-1} WHERE name = "{name}"')
                    self.__db.commit()
                    return True


        except Exception as e:
            print('Помилка оновлення значення', e)

    
    def countsUpdate(self):
        try:
            self.__cursor.execute('UPDATE users SET countchoice = 5')
            self.__db.commit()


        except Exception as e:
            print('Помилка оновлення спроб', e)