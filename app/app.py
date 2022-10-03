#./app/app.py
from flask import Flask, Response, render_template
from bson.json_util import dumps
from pymongo import MongoClient
import os

PEOPLE_FOLDER = os.path.join('static', 'pato')

app = Flask(__name__,static_folder='/app/static',template_folder='/app/templates')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER  

# Conectar al servicio (docker) "mongo" en su puerto estandar
client = MongoClient("mongo", 27017)

# Base de datos
db = client.cockteles

#######################################################################
    
@app.route('/')
def index():
 	return '/imagen -> Imprime una imagen en pantalla    || /fibonacci/*numero* -> Función fibonacci    || /todas_las_recetas -> todas las recetas de "Cockteles"'

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

#######################################################################

@app.route('/todas_las_recetas')
def mongo():
    # Encontramos los documentos de la coleccion "recipes"
    recetas = db.recipes.find() # devuelve un cursor(*), no una lista ni un iterador

    lista_recetas = []
    for  receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    # Convertimos los resultados a formato JSON
    resJson = dumps(response)

    # Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
    return Response(resJson, mimetype='application/json')

#######################################################################

@app.route('/recetas_con/<string:ingrediente>')
def busca_ingrediente(ingrediente):
	# Encontramos los documentos de la coleccion "recipes"
	recetas = db.recipes.find({"ingredients.name": ingrediente}) # devuelve un cursor(*), no una lista ni un iterador

	lista_recetas = []
	for  receta in recetas:
		app.logger.debug(receta)  # salida consola
		lista_recetas.append(receta)

	response = {
		'len': len(lista_recetas),
		'data': lista_recetas
	}

	# Convertimos los resultados a formato JSON
	resJson = dumps(response)

	# Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
	return Response(resJson, mimetype='application/json')

#######################################################################

@app.route('/recetas_compuestas_de/<int:numero>/ingredientes')
def busca_num_ingrediente(numero):
	# Encontramos los documentos de la coleccion "recipes"
	recetas = db.recipes.find( { "ingredients": { "$size": 2 } } ) # devuelve un cursor(*), no una lista ni un iterador

	lista_recetas = []
	for  receta in recetas:
		app.logger.debug(receta)  # salida consola
		lista_recetas.append(receta)

	response = {
		'len': len(lista_recetas),
		'data': lista_recetas
	}

	# Convertimos los resultados a formato JSON
	resJson = dumps(response)

	# Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
	return Response(resJson, mimetype='application/json')
