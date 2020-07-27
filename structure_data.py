#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 21:11:25 2020

@author: lucasmarchioro


"""

import requests
import pandas as pd
import numpy as np

class PokemonInfo:
    def __init__(self, poke_number):
        self.id = poke_number
        self.api = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(poke_number) + '/')
        
    def basic_info(self):
        try:
            api = self.api
        except:
            print('pokemon doesnt exist')
        df = pd.json_normalize(api.json(), sep = "_", max_level = 1)

        #Seleciona apenas colunas sem arrays/imporantes
        cols_select = ['id', 'name', 'order', 'height']
        df = df[cols_select]
        value = df.loc[0,'id']

        #pega o tipo dos pokemons
        df_types = pd.json_normalize(api.json(), record_path = 'types', sep = "_", max_level = 1)
    
        #testa se o pokemon possui dois Tipos         
        try:
            type2 = [df_types.loc[1, 'type_name']]
        except:
            type2 = np.nan

        data = {'Type1':[df_types.loc[0, 'type_name']],
                'Type2':type2}
    
        df_types = pd.DataFrame(data=data)
        df_types['id'] = value
    
        #Joga tudo para a mesma base de cadastro:
            #Infos unicas + Tipos
        df = pd.merge(df, df_types, on = 'id', how = 'left')
        
        return df

    def stats_info(self):
        
        df_stats = pd.json_normalize(self.api.json(), record_path = 'stats', sep = "_")
        df_stats['id'] = self.id
        #Transforma base de linha para colunar, para que cada linha seja caracterizada por um ID
        df_stats = pd.pivot_table(df_stats, values = 'base_stat', columns ='stat_name',
                          index = 'id')
        df_stats['total_stats'] = (df_stats['attack'] + df_stats['defense'] +
                            df_stats['special-attack'] +
                            df_stats['special-defense'] +
                            df_stats['speed'] + df_stats['hp'])
        return df_stats

#Cria DataFrame com todos os pokemons
lst = []
lst_stats = []
for pokeIndex in range(1, 808):
    poke = PokemonInfo(pokeIndex)
    
    df = poke.basic_info()
    df_stats = poke.stats_info()
    
    lst.append(df)
    lst_stats.append(df_stats)
    
    print(pokeIndex)

dft = pd.concat(lst)
df_statst = pd.concat(lst_stats)
