#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
This script uses KAYAK to search for flights in hard-coded configurations, 
given by <TIPO>. It searches the next date from the provided one <DATA>, 
and it searches <N_SEMANAS> weeks after this date. If <N_SEMANAS> is not 
provided, it searches only in the next available date from <DATA>.

USAGE:    flight-search.py <TIPO> <DATA> [<N_SEMANAS>]
EXAMPLES: flight-search.py semana 2019-07-06
          flight-search.py semana 2019-07-06 4
          flight-search.py findi  2019-08-21

Written by: Henrique S. Xavier, hsxavier@if.usp.br, 04/mai/2019.
"""

import sys
import subprocess
import datetime as dt
import time

# Hard-coded:
navegador = 'firefox'
instance  = '--new-tab'
# Parâmetros do vôo:
trajeto    = 'BSB-CGH'
stops      = '0'

# Configurações de viagens de um final de semana:
# (idia: = day of the week; hmin = earliest flight time; hmax = latest flight time)
# Time format: %H%M
# Days #: 0 = Monday, 1 = Tuesday, ...
saida_qui   = {'idia':3, 'hmin':'1730', 'hmax':'2130'}
saida_sex   = {'idia':4, 'hmin':'1730', 'hmax':'2130'}
chegada_seg = {'idia':0, 'hmin':'0830', 'hmax':'1100'}
chegada_dom = {'idia':6, 'hmin':'1800', 'hmax':'2100'}
# Configurações de viagens de uma semana:
chegada_qui = {'idia':3, 'hmin':'0830', 'hmax':'1130'}
chegada_qua = {'idia':2, 'hmin':'1730', 'hmax':'2130'}


# Tipos de viagens:
findi        = {'saidas':[saida_qui, saida_sex], 'chegadas':[chegada_dom, chegada_seg]}
semana       = {'saidas':[saida_qui, saida_sex], 'chegadas':[chegada_qua, chegada_qui]}
menu_viagens = {'findi':findi, 'semana':semana} 


###############
### Funções ###
###############

# Link para o kayak:
def kayak_link(trajeto, ida_data, ida_hmin, ida_hmax, volta_data, volta_hmin, volta_hmax, stops):
    url = 'https://www.kayak.com.br/flights/'+trajeto+\
          '/'+ida_data+'/'+volta_data+'?sort=price_a&fs=takeoff='+ida_hmin+','+ida_hmax+'_'+volta_hmin+','+volta_hmax+';stops='+stops+';providers=-SKYTOURS'
    return url

# Retorna a data do próximo dia da semana (2a=0, 3a=1, 4a=2, 5a=3, 6a=4, Sáb=5, Dom=6)
# a partir de uma data inicial:
def prox_dia(data, idia_semana):
    dia0_semana = data.weekday()
    if idia_semana > dia0_semana:
        delta_dias = idia_semana - dia0_semana
    else:
        delta_dias =  7 + idia_semana - dia0_semana
    return data + dt.timedelta(days=delta_dias)


########################
### Código principal ###
########################

# Docstring output:
if len(sys.argv) != 1 + 2 and len(sys.argv) != 1 + 3: 
    print(__doc__)
    sys.exit(1)

# Pega input:
tipo_viagem = sys.argv[1]
data_input  = sys.argv[2]
if len(sys.argv) == 1 + 2:
    n_semanas = 1
else:
    n_semanas = int(sys.argv[3])

# Pega a data atual:
hoje = dt.datetime.today()
# Pega a data de viagem:
dataY, dataM, dataD = data_input.split('-')

# Loop sobre semanas a partir da data de input:
data_inicial = dt.datetime(int(dataY), int(dataM), int(dataD)) - dt.timedelta(days=1)
for i in range(n_semanas):
    data_semana = data_inicial + dt.timedelta(days=i*7)
    #print 'data_semana:', data_semana.strftime('%Y-%m-%d')
    # Loop sobre dias possíveis de viagem:
    for saida in menu_viagens[tipo_viagem]['saidas']:
        for chegada in menu_viagens[tipo_viagem]['chegadas']:
            # Pega dias de viagem:
            data_ida0  = prox_dia(data_semana, saida['idia'])
            data_ida   = data_ida0.strftime('%Y-%m-%d')
            data_volta = prox_dia(data_ida0,   chegada['idia']).strftime('%Y-%m-%d')
            #print 'ida:', data_ida, ' volta:', data_volta
            # Busca por vôos:
            url = kayak_link(trajeto, data_ida, saida['hmin'], saida['hmax'], data_volta, chegada['hmin'], chegada['hmax'], stops)
            #print(url)
            subprocess.call([navegador, instance, url])
            #time.sleep(1)
