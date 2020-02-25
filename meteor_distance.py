#Tentar fazer um com enchentes em SP


# Browser pega uma request de uma URL e te da uma response
# Python modulo requests faz essa etapa
# Existe duas partes para ter uma response: o Verb (Get, Post) e a URL(htttp)
import requests
import math

requests.get('http://nasa.gov') #<Response [200]> significa que foi um sucesso, mas precisamos ver a DATA que foi enviada para gente

resp = requests.get('http://nasa.gov')

resp.status_code #codigo da responde (nesse caso 200)

resp.text #pega o codigo da pagina da response

#mas um código html não é valido ou a melhor opção para se pegar data, apenas para mostrar num browser
#existe 4 maneiras de pegar data, da pior para a melhor: 
#1: O Scraping WebPages (Processar o html da pagina para pegar informações | Muito Dificil e cansativo, tem que ser usado como ultima opção | Há um modulo chamado "beautiful soup" que ajuda com isso )
#2: Algumas empresas deixa fazer o Download de algo mais estruturado, tipo um JSON ou XML, para voce dar um Parse no Data e trabalhar com o código. Funciona, mas você está baixando o conteudo todo e pode se tornar ineficiente
#3: Pode usar uma API se o Site usar. É bem melhor, mas alguns sites tem API de baixo nivel e dificeis de usar. Usualmente vai te devolver um JSON ou XML
#4: pODE TER UMA lIBRARY OU pACKAGE para python, como a amazon web services ou o boto3, que ajudar a recuperar data

# Exemplo: Quero saber se há uma chance de Meteoritos caírem onde eu moro, a Nasa mantém registro disso e eu posso utilizar

# Eu preciso quebrar o problema em pequenas partes: 1° pegar a Data, 2° transformar em uma estrutura em python para ler, 3°Calcular a distancia do mais proximo meteorito e onde eu moro, 4° Preciso classicar a Data pela distancia para achar as distancias mais proximas, 5° eu preciso colocar um top 10 das mais proximas a mim



# Pegar a data: O site da NAsa provide uma API com o retorno em JSON

meteor_resp= requests.get('https://data.nasa.gov/resource/gh4g-9sfh.json')

meteor_resp.status_code
meteor_resp.text # denso, mais dá para entender se pegar um JSON, mas sabemos que o python tem Dictionaries e Lists

# Transformar em algo que o Python saiba ler
# O Modulo Requests vem com uma função que ajuda 
meteor_resp.json()# Se você for ver, o python fez uma List ( [] ) e colocou varios Dictionaries( {} )
# As chaves batem com os ids da tabela no sire da Nasa e o valor é a Data que precisamos

meteor_data = meteor_resp.json() # Como é uma List, podemos percorrer ela

for meteor in meteor_data: print(type(meteor)) # cada dado na List é um Dict

#olhando apenas um item
meteor_data[0] # ele mostra um json com a Latitude e Longitude, mas onde podemos enteder onde se localiza? no site https://www.findlatitudeandlongitude.com/ 

# Como achar a distancia entre a data e onde eu estou? Tem uma formular para calcular isso
#  o "\" no def  é um jeito de quebrar a linha e transformar em varias linhas de codigo

 # função necessita de Floats para funfar
def calc_dist(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin( (lat2 - lat1) / 2 ) ** 2 + \
      math.cos(lat1) * \
      math.cos(lat2) * \
      math.sin( (lon2 - lon1) / 2 ) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))

calc_dist(50.775000, 6.083330 , -23.55052 , -46.633309)  # vai retornar 9290.332954565614 ou seja quasw 10KM de distancia

my_loc = (-23.55052 , -46.633309)

#como a localização utiliza floats, podemos transformar os "reclat e reclon" que são Strings em floats 
float(meteor_data[0]['reclat']) # transforma apenas reclat em float

# podemos fazer um loop para percorrer a List e adicionar um novo Valor com a distancia no Dictionary
# exemplo : meteor[0].get('reclat', 0) --> se não achar iria retornar 0

#alguns meteoros não tem Latitude ou Longitude, então o código daria erro se procurasse apenas reclat e reclon, para isso poderiamos adicionar reclat e reclon em todos, mas ai eles teriam de ter um local

for meteor in meteor_data:
    if not('reclat' in meteor and 'reclong' in meteor): continue # assim se ele não achar um Dict com lat e long ele pula aquele item
    meteor['distance'] = calc_dist(float(meteor['reclat']) , float(meteor['reclong']) , -23.55052 , -46.633309)

# Fazer uma lista de meteoritos que cairam mais proximo possivel
# poderia ser feito com .sort(), mas como nossa lista é feita de dictionaries não tem como o python saber qual é qual, a menos que contemos a ele
# Precisamos de uma maneira de contar qual é a prioridade dos Dicts
# Existe o parametro KEY que pega uma função e nota o item em uma lista

def get_dist(meteor):
    return meteor.get('distance', math.inf) # algumas dicts não tem distancia, então se ele for dar erro ele retornará um valor infinito

meteor_data.sort(key=get_dist) #passando o parametro, ele vai organizar segundo o menor numero referente aquele parametro
# Não está chamando a função get_dist, ele está passando o nome por um parametro
#Voce pode passar funções para outra funções

meteor_data[0:10] #começa no 0 e termina no 9


 
