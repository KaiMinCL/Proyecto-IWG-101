import requests
from bs4 import BeautifulSoup

#Usamos requests con la funcion get y status code para saber si podemos
#acceder a la pagina , si status_code retorna 200 estamos bien.

#print(result.status_code)


#Con esta funcion recopilamos el nombre,dificultad,url de las recetas
#que entrega la primera pagina de cada categoria de la pagina.
def extraccion_1(pagina):
    result = requests.get(pagina)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    temporal = dict()

    for div in soup.find_all("div","resultado link"):
        link = div.find("a")["href"]
        Receta = div.find("a").text.strip()
        dificultad =div.find_all("div","info_snippet",recursive=False)[0].text.strip()
        if Receta not in temporal:
            temporal[Receta]= dict()
        temporal[Receta]["url"]= link
        temporal[Receta]["dificultad"]=dificultad
    return temporal

#Creamos un solo diccionario con las recetas sin repetir de cada categoria (primera pagina
#                                                                          de cada una)
#Como solo tenemos los link que llevan a cada receta falta terminar esa seccion con
#scrapping
def organizar_resultados(lista):
    diccionario = dict()
    contador=0
    for temporal in lista:
        for receta in temporal:
            if receta not in diccionario:
                diccionario[receta]=dict()
                diccionario[receta]["url"]=temporal[receta]["url"]
                diccionario[receta]["dificultad"]=temporal[receta]["dificultad"]
            if receta in diccionario:
                contador=contador+1
    print("se repitieron: "+str(contador)+ " recetas")
    return diccionario

#Listado_url contendrá todas las url de todas las categorias que provee la pagina.
#Listado_resultados recibe los resultado de extraccion_1 al enviarle el link de
#cada categoria
listado_url = list()
lista_resultados = list()
recetario = dict()
result =requests.get("https://www.recetasgratis.net/")
src = result.content
soup = BeautifulSoup(src, 'lxml')
for div in soup.find_all("div","categoria ga"):
    listado_url.append(div.find("a")["href"])

for url in listado_url :
    aux = extraccion_1(url)
    lista_resultados.append(aux)

recetario = organizar_resultados(lista_resultados)
#Ejemplo del diccionario:
aux = extraccion_1(url)
print("SECCION DEL DICCIONARIO\n")
print(aux)


