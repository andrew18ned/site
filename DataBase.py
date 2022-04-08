from random import randint
from flask import flash
from datetime import datetime
import math
import sqlite3


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()


    def showallaccounts(self):
        try:
            self.__cursor.execute(f'SELECT name, dick FROM users ORDER BY dick DESC;')
            result = self.__cursor.fetchall()
            if result:
                return result

        except Exception as e:
            print('Помилка читання всіх гравців', e)


    def play(self, name):
        random_length = randint(-20, 20)
        try:
            for i in self.__cursor.execute(f"SELECT dick, countchoice FROM users \
                                                WHERE name = '{name}'"):
                balance = i['dick']
                update = i['countchoice'] 
                if i['countchoice'] <= 0:
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


    def getUserByEmail(self, email):
        try:
            self.__cursor.execute(f'SELECT * FROM users WHERE email = "{email}" LIMIT 1')
            result = self.__cursor.fetchone()
            if not result:
                print('User not found')
                return False

            return result
        except sqlite3.Error as e:
            print('Error get datas on DB', e)
        
        return False


    def addUser(self, name, email, hashpassword):
        try:
            self.__cursor.execute(f'SELECT COUNT() as `count` FROM users WHERE email LIKE "{email}"')
            result = self.__cursor.fetchone()

            if result['count'] > 0:
                print('Користувач з таким емейлом існує!')
                return False

            tm = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
            self.__cursor.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?, NULL, ?)', (name, email, hashpassword, 0, 5, tm))
            self.__db.commit()

        except sqlite3.Error as e:
            print('Помилка додавання в БД', e)
            return False
        
        return True


    def getUser(self, user_id):
        try:
            self.__cursor.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            result = self.__cursor.fetchone()
            if not result:
                print('User not found')
                return False

            return result
        except sqlite3.Error as e:
            print('Error get datas on DB', e)
        
        return False


    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False
        
        try: 
            binary = sqlite3.Binary(avatar)
            self.__cursor.execute(f'UPDATE users SET avatar = ? WHERE id = ?', (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Помилка оновлення аватару в БВ', e)
            return False

        return True