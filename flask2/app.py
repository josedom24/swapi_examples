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
		if tipo=="personajes":
			info2=convtipo("planetas")
			r=requests.get(doc["homeworld"])
			if r.status_code == 200:
				doc2=r.json()
				nombre=doc2[info2["nombre"]]
			url=conv_urls([doc["homeworld"]],"planetas")[0]
			doc["homeworld"]='<a href="%s">%s</a>'%(url,nombre)
		return render_template("detalle.html",datos=doc,id=id,info=info)

@app.route('/<string:tipo1>/<int:id>/<string:tipo2>')
def datos(tipo1,id,tipo2):
	info1=convtipo(tipo1)
	info2=convtipo(tipo2)
	r=requests.get(URL_BASE+info1["url"]+'/%d'%id)
	if r.status_code == 200:
		doc = r.json()  
		urls=doc[info2["dato"]]
		datos=[]
		for url in urls:
			r=requests.get(url)
			if r.status_code == 200:
				doc2=r.json()
				datos.append(doc2[info2["nombre"]])
		urls=conv_urls(urls,tipo2)
		return render_template("lista.html",datos=zip(datos,urls),id=id,title=doc[info1["nombre"]],subtitle=info2["titulo"],tipo1=tipo1,tipo2=tipo2)
    

def convtipo(tipo):
	if tipo=="peliculas":
		info={"url":"films","nombre":"title","titulo":"Películas","dato":"films"}
		detalle=(("Episodio:","episode_id"),("Nombre:","title"),("Como empeza:","opening_crawl"),("Director:","director"),("Productor:","producer"),("Fecha de lanzamiento:","release_date"))
		listas=("Personajes","Planetas","Naves","Vehiculos","Especies")

	elif tipo=="planetas":
		info={"url":"planets","nombre":"name","titulo":"Planetas","dato":"planets"}
		detalle=("Periodo de rotación:":"rotation_period")
		listas=()
	elif tipo=="vehiculos":
		info={"url":"vehicles","nombre":"name","titulo":"Vehículos","dato":"vehicles"}
		detalle=()
		listas=()
	elif tipo=="naves":
		info={"url":"starships","nombre":"name","titulo":"Naves","dato":"starships"}
		detalle=()
		listas=()
	elif tipo=="personajes":
		info={"url":"people","nombre":"name","titulo":"Personajes","dato":"characters"}
		detalle=(("Nombre:","name"),("Altura:","height"),("Peso:","mass"),("Color del pelo:","hair_color"),("Color de la mañana:","skin_color"),("Color de los ojos:","eye_color"),("Año de nacimiento:","birth_year"),("Genero:","gender"),("Planeta de origen:","homeworld"))
		listas=("Peliculas","Naves","Vehiculos","Especies")
	elif tipo=="especies":
		info={"url":"species","nombre":"name","titulo":"Especies","dato":"species"}	
		detalle=()
		listas=()
	info["tipo"]=tipo
	info["detalle"]=detalle
	info["listas"]=listas
	return info

def conv_urls(urls,tipo):
	new_url=[]
	for url in urls:
		path=url.split("/")
		print(path)
		new_url.append('/'+tipo+'/'+path[len(path)-2])
	return new_url


if __name__ == '__main__':
    app.run(debug=True)

