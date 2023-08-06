
import requests
import os

#retorna o nome do ficheiro da base de dados
def nome_ficheiro():
  return "CETEM publico 2019"


#faz download de uma base de dados para um ficheiro
def download():
  #url do ficheiro, hardcoded por enquanto
  url = "http://bit.do/cetem2019"
  #fazer pedido da base de dados ao url especificado
  data = requests.get(url)
  #escrever dados num ficheiro
  home_path = os.environ['HOME']
  folder = home_path + "/.cetem_publico"
  os.makedirs(folder,exist_ok=True)
  filename = folder +"/cetem_publico_10k.txt"
  open(filename,"wb").write(data.content)
