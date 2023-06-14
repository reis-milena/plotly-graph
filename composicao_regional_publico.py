"""
Project: Atlas do Estado Brasileiro

ADEB - XXX - Tabela 4 

Created on June 2023

@author: B... - Milena Reis
"""

#Python  Libraries
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# import psycopg2
import warnings
warnings.filterwarnings('ignore')
# import socket


# import plotly.figure_factory as ff
# from cryptography.fernet import Fernet

# Importing data
    
total_brasil = pd.read_csv("C:/Users/ville/Downloads/vinculos_publicos_br.csv",
                           sep = ";")
    
total_regiao = pd.read_csv("C:/Users/ville/Downloads/vinculos_publicos_regiao.csv",
                           sep = ";")
    
total_uf     = pd.read_csv("C:/Users/ville/Downloads/vinculos_publicos_uf.csv",
                           sep = ";")
    

# Organizing data

## Checking if it's equal

# brasil = 4837194
total_uf.query('ano == 1985')['vinculos_publicos'].sum()
total_regiao.query('ano == 1985')['vinculos_publicos'].sum()

# brasil = 10890056
total_uf.query('ano == 2019')['vinculos_publicos'].sum()
total_regiao.query('ano == 2019')['vinculos_publicos'].sum()

## Creating variable of %

anos = total_brasil.ano

###Regiao
percentual_regiao = []

for ano_i in anos:
    
    filter_ano = total_regiao['ano']== ano_i

    percentual_regiao.append(
        list(round((total_regiao[filter_ano]['vinculos_publicos']/
               total_regiao[filter_ano]['vinculos_publicos'].sum())*100,2))
        )
del ano_i
#setting list of lists into one list
percentual_regiao = pd.DataFrame(sum(percentual_regiao, []),
                                 columns = ["percent"])

total_regiao = pd.concat([total_regiao,percentual_regiao],
                         axis = 1)
del filter_ano

###UF por regiao
codigo_reg = total_uf.codigo // 10
total_uf['codigo_reg'] = codigo_reg

codigo_reg = total_uf['codigo_reg'].unique()
# percentual_uf = []
df_final_percentual = pd.DataFrame(columns=["percent_reg"])

for ano_i in anos:
    
    filter_ano = total_uf[total_uf['ano']== ano_i]
    # print(ano_i)
    
    for cod_reg in range(1,6):
        # print(codigo_reg)
        
        filter_ano_reg = filter_ano[filter_ano['codigo_reg']== cod_reg]
        
        percentual_uf = round((filter_ano_reg['vinculos_publicos']/
                               filter_ano_reg['vinculos_publicos'].sum())*100,2)
        
        percentual_uf = pd.DataFrame(percentual_uf).rename(
            columns={"vinculos_publicos":"percent_reg"})
        
        df_final_percentual = df_final_percentual.append(percentual_uf)

        # percentual_uf.append(
        #     list(round((filter_ano_reg['vinculos_publicos']/
        #                 filter_ano_reg['vinculos_publicos'].sum())*100,2)
        #          )
                 
        #     )
del ano_i, cod_reg

total_uf = total_uf.join(df_final_percentual)
#setting list of lists into one list

# percentual_uf = pd.DataFrame(sum(percentual_uf, []),
#                                  columns = ["percent_reg"])

# total_uf = pd.concat([total_uf,percentual_uf],
#                          axis = 1)

del filter_ano, filter_ano_reg, codigo_reg, df_final_percentual
###UF por Brasil

percentual_uf = []

for ano_i in anos:
    
    filter_ano = total_uf[total_uf['ano']== ano_i]
    
    percentual_uf.append(
            list(round((filter_ano['vinculos_publicos']/
                        filter_ano['vinculos_publicos'].sum())*100,2)
                 )
            )
del ano_i
#setting list of lists into one list

percentual_uf = pd.DataFrame(sum(percentual_uf, []),
                                 columns = ["percent_br"])

total_uf = pd.concat([total_uf,percentual_uf],
                         axis = 1)
del filter_ano, anos, percentual_regiao, percentual_uf

## Creating column with name of UF or Regiao

total_regiao["nome_regiao"] = total_regiao["regiao"].replace({'CO':'Centro-Oeste',
                                                              'NE':'Nordeste',
                                                              'N' :'Norte',
                                                              'SE':'Sudeste',
                                                              'S':'Sul' })
total_uf["nome_uf"] = total_uf["uf"].replace({'AC':'Acre',
                                              'AL':'Alagoas',
                                              'AP':'Amapá',
                                              'AM':'Amazonas',
                                              'BA':'Bahia',
                                              'CE':'Ceará',
                                              'DF':'Distrito Federal',
                                              'ES':'Espirito Santo',
                                              'GO':'Goiás',
                                              'MA':'Maranhão',
                                              'MT':'Mato Grosso',
                                              'MS':'Mato Grosso do Sul',
                                              'MG':'Minas Gerais',
                                              'PR':'Paraná',
                                              'PB':'Paraíba',
                                              'PA':'Pará', 
                                              'PE':'Pernambuco', 
                                              'PI':'Piauí',
                                              'RN':'Rio Grande do Norte', 
                                              'RS':'Rio Grande do Sul', 
                                              'RJ':'Rio de Janeiro', 
                                              'RO':'Rondônia',
                                              'RR':'Roraima',
                                              'SC':'Santa Catarina', 
                                              'SE':'Sergipe', 
                                              'SP':'São Paulo',
                                              'TO':'Tocantins'})

## Changing from long to wide

total_regiao_wide = pd.pivot(total_regiao, index = "ano",
                             columns = "nome_regiao",
                             values = "percent"
                             )
total_regiao_wide = total_regiao_wide.reset_index()

total_uf["nome_regiao"] = total_uf["codigo_reg"].replace({5:'Centro-Oeste',
                                                          2:'Nordeste',
                                                          1:'Norte',
                                                          3:'Sudeste',
                                                          4:'Sul' })
total_uf_wide_reg = []

for regiao in ('Centro-Oeste','Nordeste','Norte','Sudeste','Sul'):
    # print(regiao)
    dados = total_uf[total_uf.nome_regiao == regiao]
    total_uf_wide_reg.append( pd.pivot(dados, index = ["ano"],
                                           columns = "nome_uf",
                                           values = "percent_reg"
                                           ).reset_index()
                             )

total_uf_wide_br = []

for regiao in ('Centro-Oeste','Nordeste','Norte','Sudeste','Sul'):
    print(regiao)
    dados = total_uf[total_uf.nome_regiao == regiao]
    total_uf_wide_br.append( pd.pivot(dados, index = ["ano"],
                                           columns = "nome_uf",
                                           values = "percent_br"
                                           ).reset_index()
                             )
del dados, regiao

# Graph

fig = go.Figure()
    
#REGIAO

for regiao in ('Centro-Oeste','Nordeste','Norte','Sudeste','Sul'):
    fig.add_trace(go.Bar(x=total_regiao_wide['ano'], 
                         y=total_regiao_wide[regiao],
                         text= [str(f'{z}') + "%"
                                for z in total_regiao_wide[regiao].values ], 
                         name = regiao,
                         hoverinfo='name + text + x',
                         visible = True))
# fig.update_layout(barmode = "stack")



#UF por regiao

for regiao in range(5):
    # print(regiao)
    for uf in ('Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Distrito Federal',
               'Espirito Santo','Goiás','Maranhão','Mato Grosso','Mato Grosso do Sul',
               'Minas Gerais','Paraná','Paraíba','Pará', 'Pernambuco','Piauí',
               'Rio Grande do Norte','Rio Grande do Sul','Rio de Janeiro','Rondônia',
               'Roraima','Santa Catarina','Sergipe','São Paulo','Tocantins'):
        if uf in total_uf_wide_reg[regiao].columns:
            fig.add_trace(go.Bar(x=total_uf_wide_reg[regiao]['ano'], 
                                 y=total_uf_wide_reg[regiao][uf],
                                 text= [str(f'{z}') + "%"
                                        for z in total_uf_wide_reg[regiao][uf].values ], 
                                 name = uf,
                                 hoverinfo='name + text + x',
                                 visible = False))
            
#UF por Brasil

for regiao in range(5):
    # print(regiao)
    for uf in ('Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Distrito Federal',
               'Espirito Santo','Goiás','Maranhão','Mato Grosso','Mato Grosso do Sul',
               'Minas Gerais','Paraná','Paraíba','Pará', 'Pernambuco','Piauí',
               'Rio Grande do Norte','Rio Grande do Sul','Rio de Janeiro','Rondônia',
               'Roraima','Santa Catarina','Sergipe','São Paulo','Tocantins'):
        if uf in total_uf_wide_br[regiao].columns:
            fig.add_trace(go.Bar(x=total_uf_wide_br[regiao]['ano'], 
                                 y=total_uf_wide_br[regiao][uf],
                                 text= [str(f'{z}') + "%"
                                        for z in total_uf_wide_br[regiao][uf].values ], 
                                 name = uf,
                                 hoverinfo='name + text + x',
                                 visible = False))
# fig.update_layout(barmode = "stack")
    
# localidades da composicao
localidades = ['Região por Brasil', #5 traces
               "UF por Centro-Oeste", "UF por Nordeste", "UF por Norte", 
               "UF por Sudeste", "UF por Sul", 
               'Centro-Oeste por Brasil','Nordeste por Brasil','Norte por Brasil',
               'Sudeste por Brasil','Sul por Brasil']


anoFinal = total_uf_wide_reg[0].ano.max()

labels = [
    dict(xref='paper', yref='paper', x=0.02, y=-0.04, xanchor='left', yanchor='top',
         text='Fonte: RAIS/ME. Elaboração e cálculos: Atlas do Estado Brasileiro - IPEA.',
         font=dict(family='Arial', size=12, color='rgb(150,150,150)'), showarrow=False) ,
    dict(xref='paper', yref='paper', x=1.02, y=1,
         xanchor='left', yanchor='top',
         text='<b>Composição por área</b>',
         font=dict(family='Arial', size=14, color='black'), showarrow=False)
         ]

colunas_regiao = [len(total_uf_wide_br[0].columns)-1,len(total_uf_wide_br[1].columns)-1,
                  len(total_uf_wide_br[2].columns)-1,len(total_uf_wide_br[3].columns)-1,
                  len(total_uf_wide_br[4].columns)-1]

index = [0]
index.extend(range(0,5))
index.extend(range(0,5))

estado_reg, estado_br = [],[]
for localidade, indice in zip(localidades, index):
    print(localidade)
    print(indice)
    # Add dropdown
    if localidade == 'Região por Brasil':
        regiao = dict(label=f"<b>{localidade}</b>", method="update",
                    args=[{"visible": [True]*5 +[False]*27*2},
                         {"annotations": 
                          ([dict(xref='paper', yref='paper', y=1.08, xanchor='center', yanchor='bottom',
                                  text=f'{localidade}: Composição regional do emprego público total (federal, estadual e municipal) (1985-{anoFinal})',
                                  font=dict(family='Arial', size=19, color='rgb(37,37,37)'), showarrow=False),
                            dict(xref='paper', yref='paper', x=-0.03, y=0.4,
                              xanchor='left', yanchor='bottom',
                              text='%',
                              font=dict(family='Arial', size=14),
                              showarrow=False,
                              textangle=270),
                          ] + labels)}])
    elif localidade[:6//1] == 'UF por':
        
        # for indice in range(0,5):
        estado_reg.append(
            dict(label=f"<b>{localidade}</b>", method="update",
                 args=[{"visible": [False]*5 + 
                        sum(colunas_regiao[0:indice]) *[False] + 
                        colunas_regiao[indice]*[True] + 
                        sum(colunas_regiao[indice+1:len(colunas_regiao)]) *[False]
                        +[False]*27},
                       #  {"yaxis": {"tickprefix": "R$ ", "ticksuffix" : " mil"}},
                       {"annotations":
                        ([dict(xref='paper', yref='paper', y=1.08, xanchor='center', yanchor='bottom',
                               text=f'{localidade}: Composição regional do emprego público total (federal, estadual e municipal) (1985-{anoFinal})',
                               font=dict(family='Arial', size=19, color='rgb(37,37,37)'), showarrow=False),
                          dict(xref='paper', yref='paper', x=-0.03, y=0.4,
                               xanchor='left', yanchor='bottom',
                               text='%',
                               font=dict(family='Arial', size=14),
                               showarrow=False,
                               textangle=270),
                          ] + labels)}])
                )
    else:
        # for indice in range(0,5):
       estado_br.append(
           dict(label=f"<b>{localidade}</b>", method="update",
                args=[{"visible":[False]*5 + [False]*27 +
                       sum(colunas_regiao[0:indice]) *[False] + 
                       colunas_regiao[indice]*[True] + 
                       sum(colunas_regiao[indice+1:len(colunas_regiao)]) *[False]},
                      #  {"yaxis": {"tickprefix": "R$ ", "ticksuffix" : " mil"}},
                      {"annotations":
                       ([dict(xref='paper', yref='paper',  y=1.08, xanchor='center', yanchor='bottom',
                              text=f'{localidade}: Composição regional do emprego público total (federal, estadual e municipal) (1985-{anoFinal})',
                              font=dict(family='Arial', size=19, color='rgb(37,37,37)'), showarrow=False), # Título
                         dict(xref='paper', yref='paper', x=-0.03, y=0.4,
                              xanchor='left', yanchor='bottom',
                              text='%',
                              font=dict(family='Arial', size=14),
                              showarrow=False,
                              textangle=270),
                         ] + labels)}])
               )
            
# Add dropdown
fig.update_layout(updatemenus=[
        go.layout.Updatemenu(buttons=list([regiao]), 
            type='buttons',
            direction="down", pad={"r": 0, "t": 0}, showactive=False, x=1.02, 
            xanchor="left", y=0.95, yanchor="top"),
  
        go.layout.Updatemenu(
            buttons=list([x for x in estado_reg]), 
            direction="down", pad={"r": 0, "t": 0}, showactive=True, x=1.02, 
            xanchor="left", y=0.88, yanchor="top"),
         
        go.layout.Updatemenu(
            buttons=list([x for x in estado_br]),
            direction="down", pad={"r": 0, "t": 0}, showactive=True, x=1.02, 
            xanchor="left", y=0.81, yanchor="top")
            ])


fig.update_layout(annotations=[dict(xref='paper', yref='paper', y=1.08, xanchor='center', yanchor='bottom',
                                  text=f'Região por Brasil: Composição regional do emprego público total (federal, estadual e municipal) (1985-{anoFinal})',
                                  font=dict(family='Arial', size=19, color='rgb(37,37,37)'), showarrow=False),
                               dict(xref='paper', yref='paper', x=-0.03, y=0.4,
                              xanchor='left', yanchor='bottom',
                              text='%',
                              font=dict(family='Arial', size=14),
                              showarrow=False,
                              textangle=270),
                              ] + labels,
                 xaxis = dict(
                        domain=[0.02, 1],
                        tickvals = [x for x in range(1985,2020,5)] + [2019]
                    ),
                  height = 700,
                  legend=go.layout.Legend(traceorder = 'normal', x=0.5, y=1.07, orientation='h', xanchor='center'),
                  barmode='stack',
                  hovermode = 'x')


plot(fig, 
     filename="C:/Users/ville/Documents/Repositories/plotly-graph/composicao_regional_publico.html");