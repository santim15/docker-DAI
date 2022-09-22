#./app/app.py
from flask import Flask, render_template
import os

PEOPLE_FOLDER = os.path.join('static', 'pato')

app = Flask(__name__,static_folder='/app/static',template_folder='/app/templates')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER  

#######################################################################
    
@app.route('/')
def hello_world():
  return 'Hello, World!'

#######################################################################

@app.route('/imagen')
def imagen():
	full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pato.jpg')
	return render_template("index.html", user_image = full_filename)


#######################################################################

@app.route('/fibonacci/<int:lectura>')
def fibonacci(lectura):

	# var iniciales
	n1, n2 = 0, 1
	contador = 2
	aux = 0

	# check lectura positiva
	if lectura <= 0:
		return "Lectura erronea: Valor negativo"

	# check lectura = 1
	elif lectura == 1:
		return "Numero leido: 1 Numero obtenido: 0"

	# check lectura = 2
	elif lectura == 2:
		return "Numero leido: 2 Numero obtenido: 1"

	# hacer Fibonacci
	else:
		while contador < lectura:
			aux = n1 + n2
			# update values
			n1 = n2
			n2 = aux
			contador += 1
	
	resultado = "Numero leido: "
	resultado += str(lectura)
	resultado += " Numero obtenido: "
	resultado += str(aux)
	return resultado


#######################################################################

@app.errorhandler(404)
def error404(e):
    return render_template('404.html'),404
