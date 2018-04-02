import requests
from flask import Flask, url_for, request, render_template
app = Flask(__name__)   
URL_BASE="https://swapi.co/api/"

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/<string:tipo>')
def controlador(tipo):
	info=convtipo(tipo)
	r=requests.get(URL_BASE+info["url"])
	if r.status_code == 200:
		doc = r.json()    
		return render_template("list.html",datos=doc["results"],info=info)
			
@app.route('/<string:tipo>/<int:id>')
def detalle(tipo,id):
	info=convtipo(tipo)
	r=requests.get(URL_BASE+info["url"]+'/%d'%id)
	if r.status_code == 200:
		doc = r.json()    
		return render_template("detalle.html",datos=doc,id=id)

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


def convtipo(tipo):
	if tipo=="peliculas":
		info={"url":"films","nombre":"title"}
		detalle=(("Episodio:","episode_id"),("Nombre:","title"),("Como empeza:","opening_crawl"),("Director:","director"),("Productor:","producer"),("Fecha de lanzamiento:","realease_date"))
		listas=(("Personajes:","characters"),("Planetas:","planets"),("Naves:","starships"),("Vehiculos:","vehicules"),("Especies:","species"))

	elif tipo=="planetas":
		info={"url":"planets","nombre":"name"}
		detalles=()
		listas=()
	elif tipo=="vehiculos":
		info={"url":"vehicles","nombre":"name"}
		detalles=()
		listas=()
	elif tipo=="naves":
		info={"url":"starships","nombre":"name"}
		detalles=()
		listas=()
	elif tipo=="personajes":
		info={"url":"people","nombre":"name"}
		detalles=()
		listas=()
	elif tipo=="especies":
		info={"url":"species","nombre":"name"}	
		detalles=()
		listas=()
	info["tipo"]=tipo
	info["detalle"]=detalle
	info["listas"]=listas
	return info

if __name__ == '__main__':
    app.run(debug=True)

