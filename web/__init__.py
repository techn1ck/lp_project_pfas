from flask import Flask

app = Flask(__name__)
app.config.from_object('cfg')

""" Заглушка для определения ID текущего пользователя
В дальнейшем брать ID из сессии или из куков после авторизации
"""
ID_USER = 1

from web import views