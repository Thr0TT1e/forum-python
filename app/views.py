from app import app # From ищет библиотеки и папки в проекте import импортирует из библиотек и папок нужные функции
from flask import render_template
from flask import request # Глобальная переменная
from flask import redirect
from flask import make_response # Импорт

@app.route('/')
@app.route('/index')
def index():
	return "<h1>Привет МИР!</h1>"