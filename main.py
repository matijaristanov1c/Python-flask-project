from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", # ako niste nista menjali u phpmyadminu ovo su standardni
    # username i password
	database="januar2022" # iz phpmyadmin 
    )

class Biciklista:
	__id:int
	__broj_prijave:int
	__pol:str
	__sifra:str
	__etapa_jedan:int
	__etapa_dva:int


	def __init__ (self,id:int,broj_prijave:int,pol:str,sifra:str,etapa_jedan:int,etapa_dva:int):
		self.__id = id
		self.__broj_prijave = broj_prijave
		self.__pol = pol
		self.__sifra = sifra
		self.__etapa_jedan = etapa_jedan
		self.__etapa_dva = etapa_dva

	def __str__(self):
		rez = f"ID: {self.__id}\n"
		rez += f"Broj prijave: {self.__broj_prijave}\n"
		rez += f"Sifra: {self.__sifra}\n"
		rez += f"Pol: {self.__pol}\n"
		rez += f"etapa_jedan: {self.__etapa_jedan}\n"
		rez += f"etapa_dva: {self.__etapa_dva}\n"
		return rez
	
	def get_id(self):
		return self.__id
	
	def get_broj_prijave(self):
		return self.__broj_prijave
	
	def get_pol(self):
		return self.__pol

	def get_sifra(self):
		return self.__sifra
	
	def get_etapa_jedan(self):
		return self.__etapa_jedan

	def get_etapa_dva(self):
		return self.__etapa_dva
	
	def set_id(self,novi_id):
		self.__id = novi_id
	
	def set_broj_prijave(self,novi_broj):
		self.__broj_prijave = novi_broj

	def set_pol(self,novi_pol):
		self.__pol = novi_pol
	
	def set_sifra(self,nova_sifra):
		self.__sifra = nova_sifra
	
	def set_etapa_jedan(self,nova_prva):
		self.__etapa_jedan = nova_prva

	def set_etapa_dva(self,nova_druga):
		self.__etapa_dva = nova_druga

	def izracunaj_ukupno_vreme(self):
		return etapa_jedan + etapa_dva


@app.route('/register', methods =['POST','GET'])
def register():
	
	if request.method == "GET":
		return render_template(
			'register.html'
		)
	
	broj_prijave = request.form['broj_prijave']
	sifra = request.form['sifra']
	potvrda = request.form['potvrda']
	pol = request.form['pol']
	etapa_jedan = request.form['etapa_jedan']
	etapa_dva = request.form['etapa_dva']

	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM biciklisti WHERE broj_prijave=?'
	vrednost = (broj_prijave,)
	cursor.execute(sql,vrednost)

	rez = cursor.fetchone()

	if rez != None:
		return render_template(
			'register.html',
			broj_prijave_greska = 'Broj prijave vec postoji'
		)
	
	if sifra != potvrda:
		return render_template(
			'register.html',
			sifra_greska = 'Sifre se ne poklapaju'
		)
	
	if int(etapa_jedan) < 0:
		return render_template(
			'register.html',
			etapa_jedan_greska = 'Broj mora biti pozitivan'
		)
	
	if int(etapa_dva) < 0:
		return render_template(
			'register.html',
			etapa_dva_greska = 'Broj mora biti pozitivan'
		)
	
	cursor = mydb.cursor(prepared=True)
	sql = 'INSERT INTO biciklisti VALUES(null,?,?,?,?,?)'
	vrednosti = (broj_prijave,sifra,pol,etapa_jedan,etapa_dva)
	cursor.execute(sql,vrednosti)

	mydb.commit()

	return redirect(url_for('show_all'))

def konverzija(tapl):
	tapl = list(tapl)
	n = len(tapl)
	for i in range(n):
		if isinstance(tapl[i], bytearray):
			tapl[i] = tapl[i].decode()
	return tapl

@app.route('/login', methods =['POST','GET'])
def login():

	if request.method == 'GET':
		return render_template(
			'login.html'
		)

	
	broj_prijave = request.form['broj_prijave']
	sifra = request.form['sifra']

	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM biciklisti WHERE broj_prijave=?'
	vrednost =(broj_prijave,)
	cursor.execute(sql,vrednost)

	rez = cursor.fetchone()

	if rez == None:
		return render_template(
			'login.html',
			broj_prijave_greska = 'Los broj prijave'
		)
	
	rez = konverzija(rez)

	if sifra != rez[2]:
		return render_template(
			'login.html',
			sifra_greska = 'Sifre se ne poklapaju'
		)
	
	session['broj_prijave'] = broj_prijave

	return redirect(url_for('show_all'))

@app.route('/show_all')
def show_all():

	cursor = mydb.cursor(prepared=True)
	sql = 'SELECT * FROM biciklisti'
	cursor.execute(sql)
	rez = cursor.fetchall()

	n = len(rez)
	for i in range(n):
		rez[i] = konverzija(rez[i])

	lista_biciklista = []
	for element in rez:
		id = element[0]
		broj_prijave = element[1]
		sifra = element[2]
		pol = element[3]
		etapa_jedan = element[4]
		etapa_dva = element[5]
		trenutni_biciklista = Biciklista(id,broj_prijave,sifra,pol,etapa_jedan,etapa_dva)
		lista_biciklista.append(trenutni_biciklista)

	return render_template(
		'show_all.html',
		biciklisti = lista_biciklista
	)

@app.route('/logout')
def logout():

	if 'broj_prijave' in session:
		session.pop('broj_prijave')
		return redirect(url_for('login'))

	else:
		return redirect(url_for('show_all'))

app.run(debug=True)
