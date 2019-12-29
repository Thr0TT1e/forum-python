from app import app # From ищет библиотеки и папки в проекте import импортирует из библиотек и папок нужные функции
from flask import render_template
from flask import request # Глобальная переменная
from flask import redirect
from flask import make_response # Импорт
import json
import hashlib

@app.route('/')
@app.route('/index')
def index():
	file = open('forums.json', 'r', encoding='UTF-8')
	forums = json.load(file)
	file.close()
	id = request.cookies.get('user')
	file = open('users.json', 'r', encoding='UTF-8')
	users = json.load(file)
	file.close()
	for user in users:
		if id == hashlib.sha3_512(str(user['id']).encode('UTF-8')).hexdigest():
			return render_template('index.html', title="Главная страница", forums=forums, user=user)
	return render_template('index.html', title="Главная страница", forums=forums)

@app.route('/forums/<int:id>')
def forum(id):
	file = open('forums.json', 'r', encoding='UTF-8')
	forums = json.load(file)
	file.close()
	for forum in forums:
		if forum['id'] == id:
			currentForum = forum
			break
	return render_template('forum.html', title=currentForum['title'], forum=currentForum)

@app.route('/registration', methods=['POST', 'GET'])
def registration():
	if request.method == 'GET':
		return render_template('reg.html', title='Регистрация')
	else:
		file = open('users.json', 'r', encoding='UTF-8')
		users = json.load(file)
		file.close()
		users.append({
			'id': len(users) + 1,
			'login': request.form.get('login'),
			'password': hashlib.sha3_512(request.form.get('password').encode('UTF-8')).hexdigest()
		})
		file = open('users.json', 'w', encoding='UTF-8')
		json.dump(users, file)
		file.close()
		return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		login = request.form.get('login')
		password = hashlib.sha3_512(request.form.get('password').encode('UTF-8')).hexdigest()
		file = open('users.json', 'r', encoding='UTF-8')
		users = json.load(file)
		file.close()
		for user in users:
			if login == user['login'] and password == user['password']:
				response = make_response(redirect('/'))
				response.set_cookie(key='user', value=hashlib.sha3_512(str(user['id']).encode('UTF-8')).hexdigest(), max_age=60*60*24)
				return response
		return render_template('login.html', error='Нет пользователя с таким паролем!!!')
@app.route('/logout')
def logout():
	response = make_response(redirect('/'))
	response.set_cookie(key='user', value='', max_age=0)
	return response
