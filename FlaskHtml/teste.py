import urllib.request, json

url = 'https://api.themoviedb.org/3/discover/movie?sort_by=pularity.desc&api_key=3ddc9b92db4de6c6559569c67bd88a13'

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jsondata = json.loads(dados)
print(jsondata['results'])