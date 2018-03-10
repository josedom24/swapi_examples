import requests
URL_BASE="https://swapi.co/api/"
planetas=[]
r=requests.get(URL_BASE+'planets/')
if r.status_code == 200:
	doc = r.json()
	print("Número de planetas:",doc["count"])
	for resultado in doc["results"]:
		planetas.append(resultado["name"])
	pagina=2

	while doc["next"]!=None:
		payload={"page":pagina}
		r=requests.get(URL_BASE+'planets/',params=payload)
		if r.status_code == 200:
			doc = r.json()
			for resultado in doc["results"]:
				planetas.append(resultado["name"])
			pagina=pagina+1
	print("\n".join(planetas))
else:
	print("Error en la API")
