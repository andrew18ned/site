from flask import url_for
from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self
    
    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else 'Без імені'

    def getEmail(self):
        return self.__user['email'] if self.__user else 'Без email'

    def getDick(self):
        return self.__user['dick'] if self.__user else 'Без пісюна'

    def getTime(self):
        return self.__user['time'] if self.__user else 'Не визначено'

    def get_count_choice(self):
        return self.__user['countchoice'] if self.__user else 'Не визначено'

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource('static/images/defaul.png', 'rb') as f:
                    img = f.read()
            except Exception as e:
                print('Не знайдено аватар заумовчуванням',e)    
        
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext.lower() == 'png':
            return True
        return False