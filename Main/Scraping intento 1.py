import requests
from bs4 import BeautifulSoup
from time import time
import re



#Queremos cambiar la extructura de los link para poder buscar las primeras 10
#paginas de resultado.
def agregar_formato_a_link(link):
    texto= link[0:-6]
    texto= texto+"{pagina}.html"
    return texto

#Se extraen los link de cada receta de las primeras 10 paginas
#URL corresponde al link de la categoria
def extraccion_nivel_2(url):
    url= agregar_formato_a_link(url)
    listado= list()
    for i in range(1,11):
        link = url.format(pagina= i)
        result =requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        for div in soup.find_all("div","resultado link"):
            link= div.find("a")["href"]
            listado.append(link)
    return listado
        

def ban (link):
    baneados=["https://www.recetasgratis.net/receta-de-jamon-con-chorreras-67262.html",
              "https://www.recetasgratis.net/video-receta-de-sandia-con-vodka-59355.html",
              "https://www.recetasgratis.net/video-receta-de-jugo-con-fibra-59038.html"]
    if "articulo" in link or "video" in link:
            return True
    for ban in baneados:
        if link == ban:
            return True
    return False
#Temporal representa la lista total de las recetas, como se repiten en algunas
#Categorias las filtramos para tenerlas solo 1 vez.
def filtrar_repetidos(temporal,lista_10_pag):
    for link in lista_10_pag :
        if link not in temporal:
            if ban(link) == False :
                temporal.append(link)
    return temporal

#Extraccion de información de todo lo referente a una receta :D
def extraccion_nivel_3(url):
    result =requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')
    articulo = soup.find("article","columna-post")
    nombre_receta=articulo.find("h1","titulo titulo--articulo").text.strip()
    div_intro = articulo.find("div","intro")
    div_recipe_info = articulo.find("div","recipe-info")
    if div_intro.find("img"):
        imagen_producto_final = div_intro.find("img")["src"]
    else:
        imagen_producto_final = "http://images.wikia.com/ligahispana/es/images/1/1f/Imagen_no_disponible.PNG"
    if div_recipe_info.find("span","property comensales"):
        cantidad_platos = div_recipe_info.find("span","property comensales").text.strip()
    else:
        cantidad_platos = 1
    if div_recipe_info.find("span","property duracion"):
        tiempo_preparacion = div_recipe_info.find("span","property duracion").text.strip()
    else:
        tiempo_preparacion = "sin informacion"
    
    if  div_recipe_info.find("span","property dificultad"):
        dificultad = div_recipe_info.find("span","property dificultad").text.strip()
    else:
        dificultad= "sin informacion"
    
###PRIMERA PARTE FEA: CONSEGUIR INGREDIENTES
    lista_ingredientes = list()
    for li in div_recipe_info.find_all("li",{'class':"ingrediente"}):
       if li.find("label"):
           lista_ingredientes.append(li.find("label").text.strip())
###SEGUNDA PARTE FEA: CONSEGUIR LOS PASOS A SEGUIR
    #for div in articulo.find_all("div",id = True):

    lista_pasos = list()
    for div in articulo.find_all("div", {'id': re.compile(r'^anchor')}):
        for strong in div.find_all("strong"):
            strong.extract()
        if div.find("p"):
            paso = div.find("p").text
        else :
            paso = ""
        if div.find("img"):
            link_paso= div.find("img")["src"]
        else:
            link_paso ="http://images.wikia.com/ligahispana/es/images/1/1f/Imagen_no_disponible.PNG"
        lista_pasos.append( (paso,link_paso))

    return (nombre_receta,imagen_producto_final,cantidad_platos,tiempo_preparacion,
            dificultad,lista_ingredientes,lista_pasos)
    

        

def crear_database(datos):
    archivo = open("database.txt","w",encoding="utf-8")
    contador = 0
    start_up = time()
    for nombre_receta,imagen_producto_final,cantidad_platos,tiempo_preparacion,dificultad,lista_ingredientes,lista_pasos in datos:
                print("Estoy en Datos["+str(contador)+"]")
                archivo.write(nombre_receta.strip()+"---"+imagen_producto_final.strip()+"---"+str(cantidad_platos).strip()+"---"+
                         str(tiempo_preparacion).strip()+"---"+str(dificultad).strip()+"---")
                ultimo_indice = len(lista_ingredientes)-1
                actual = 0
                for ingrediente in lista_ingredientes:
                    archivo.write(ingrediente.strip())
                    if actual != ultimo_indice :
                        archivo.write(";")
                    actual = actual + 1
                archivo.write("---")
                ultimo_indice = len(lista_pasos)-1
                actual = 0
                for paso,imagen_referencia in lista_pasos:
                    archivo.write(paso.strip()+"--"+imagen_referencia.strip())
                    if actual != ultimo_indice :
                        archivo.write("___")
                    actual = actual + 1
                archivo.write("\n")
                if contador%100 == 0 :
                    print("Guardando linea: "+ str(contador) +" tiempo transcurrido: ", time()-start_up)
                contador = contador + 1
    
    archivo.close()
    print("ARCHIVO FINALIZADO!!!!!")

###############################################################################
# ACA COMIENZA EL PROGRAMA PRINCIPAL 
###############################################################################


result =requests.get("https://www.recetasgratis.net/")
src = result.content
soup = BeautifulSoup(src, 'lxml')


listado_url = list()
lista_resultados = list()
start_time = time()
#Nivel 1: Todos los link de cada categoria:
for div in soup.find_all("div","categoria ga"):
    listado_url.append(div.find("a")["href"])
print(len(listado_url))
for i in range(len(listado_url)):
    if listado_url[i] == "https://www.recetasgratis.net/Recetas-de-Consejos-de-cocina-listado_receta-6146_1.html":
        del listado_url[i]
        break
#Nivel 2: Se extraeran las primeras 10 paginas de resultado de cada categoria
temporal = list()
for url in listado_url:
    listado_de_links_10_paginas= extraccion_nivel_2(url)
    temporal = filtrar_repetidos(temporal,listado_de_links_10_paginas)
print("TOTAL DE RECETAS CAPTURADAS: ",len(temporal))
print("TIEMPO QUE TOMA EN SACAR TODOS LOS LINK: ", time()-start_time)

#Nivel 3: Tenemos el link de todas las recetas de cada categoria
#Procedemos a extraer la informacion y guardarla

datos= list()
i = 1
for link_receta in temporal[0:]:
    print("Estoy en el link ",i,":", link_receta )
    tupla = extraccion_nivel_3(link_receta)
    i= i+1
    datos.append(tupla)

    
print("TIEMPO QUE TOMA EXTRAER TODA LA INFO: ", time()-start_time)
crear_database(datos)
