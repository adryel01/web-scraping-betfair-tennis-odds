import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

'''Função para buscar odds de esportes com apenas 2 resultados possíveis'''

def busca_odds(url_betfair):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    resposta = requests.get(url_betfair, headers = headers)
    sopao = resposta.text
    organizado = BeautifulSoup(sopao, 'html.parser')
    
    lista_jogos = organizado.find_all('span', {'class':re.compile('team-name')})
    qtd_jogos = len(lista_jogos)
    
    lista_odds = organizado.find_all('span', {'class':re.compile('ui-display-decimal-price')})
    qtd_odds = len(lista_jogos)
    
    lista_total = []
    indice = 0
    lista_a = []
    lista_b = []
    for i in range(qtd_jogos):
        indice = indice + 1
        jogadores = lista_jogos[i].contents[0].text[1:-1]
        odds = float(lista_odds[i].contents[0].text[1:-1].replace('.','').ljust(3,'0'))/100
        jogo = (indice,jogadores,odds)
        lista_total.append(jogo)
        
        if indice %2 == 1:
            a = lista_total[indice-1]
            lista_a.append(a)
        
        
        
        if indice %2 == 0:
            b = lista_total[indice-1]
            lista_b.append(b)
            
    df_tabela = pd.DataFrame(lista_total, columns=['Indice', 'Jogadores', 'Odds']) 
    df_tabela_a = pd.DataFrame(lista_a, columns=['Indice', 'Jogador 1', 'Odds 1']) 
    df_tabela_b = pd.DataFrame(lista_b, columns=['Indice', 'Jogador 2', 'Odds 2']) 

    df_tabela['Odds'] = df_tabela['Odds'].astype(np.float32) 
    df_tabela_a['Odds 1'] = df_tabela_a['Odds 1'].astype(np.float32)
    df_tabela_b['Odds 2'] = df_tabela_b['Odds 2'].astype(np.float32)
    
    return df_tabela

df1 = busca_odds(input('Insira a url: '))
print(df1)
