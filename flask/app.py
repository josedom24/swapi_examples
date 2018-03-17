import requests
from flask import Flask, url_for, request, render_template
app = Flask(__name__)   
URL_BASE="https://swapi.co/api/"

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/peliculas/')
def peliculas():
	r=requests.get(URL_BASE+'films/')
	if r.status_code == 200:
		doc = r.json()    
		return render_template("peliculas.html",datos=doc["results"])
			
@app.route('/peliculas/<int:id>')
def peliculas_detalle(id):
	r=requests.get(URL_BASE+'films/%d'%id)
	if r.status_code == 200:
		doc = r.json()    
		return render_template("peliculas_detalle.html",datos=doc,id=id)

@app.route('/peliculas/<int:id>/personajes')
def peliculas_personajes(id):
	r=requests.get(URL_BASE+'films/%d'%id)
	if r.status_code == 200:
		doc = r.json()  
		url_personajes=doc["characters"]
		personajes=[]
		for url_personaje in url_personajes:
			r=requests.get(url_personaje)
			if r.status_code == 200:
				doc2=r.json()
				personajes.append(doc2["name"])

		return render_template("lista.html",datos=zip(personajes,url_personajes),id=id,title=doc["title"],subtitle="Personajes",url_return="peliculas_detalle")
    
@app.route('/peliculas/<int:id>/planetas')
def peliculas_planetas(id):
	r=requests.get(URL_BASE+'films/%d'%id)
	if r.status_code == 200:
		doc = r.json()  
		url_planetas=doc["planets"]
		planetas=[]
		for url_personaje in url_planetas:
			r=requests.get(url_personaje)
			if r.status_code == 200:
				doc2=r.json()
				planetas.append(doc2["name"])

		return render_template("lista.html",datos=zip(planetas,url_planetas),id=id,title=doc["title"],subtitle="Planetas",url_return="peliculas_detalle")


if __name__ == '__main__':
    app.run(debug=True)
