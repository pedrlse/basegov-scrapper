# imports
import requests
import math
import json
import numpy as np
from bs4 import BeautifulSoup
from lib.server_error import checkServer

# variaveis globais
loadlink = 0


def readlinks(contratos, baseurl, checkempty):  # funcao para recolha dos links

    # variaveis locais
    i = 0
    iniint = 0
    finint = 0
    global loadlink
    arraylinks = []
    numlinks = contratos
    rangeint = (numlinks - 1)

    # mostrar numero de resultados obtidos e recolhidos
    print(f'A recolher {numlinks} de {checkempty} resultados...')

    # processo caso o numero de recolhidos seja 1
    if numlinks == 1:
        # mostrar estado de conclusao
        print(str(math.trunc(loadlink)) + "%")

        link = baseurl

        r = requests.get(link)

        # mostrar erro de ligação no servidor
        checkServer(link, loadlink)

        soup = BeautifulSoup(r.text, 'lxml')

        productlist = soup.find('span', {"class": "plusSign"})

        tagA = productlist.find('a')
        link = tagA['href']
        if link not in arraylinks:
            arraylinks.append(link)

        loadlink = loadlink + 100
        print(str(math.trunc(loadlink)) + "%")
        print(len(arraylinks))
        print('Fase 1/3 Concluída')
        return arraylinks

    # processo caso o numero de recolhidos seja maior que 1
    else:
        while i < rangeint:
            # mostrar estado de conclusao
            print(str(math.trunc(loadlink)) + "%")
            if (numlinks < 100):
                loadlink = 100
            else:
                loadlink = loadlink + 100/numlinks*100
            i = i + 100

            if (i > rangeint):
                finint = rangeint
                if ((iniint != 0) and ((iniint % 10) == 0)):
                    iniint = iniint + 1
                if finint == iniint:
                    iniint = iniint - 1
            else:
                finint = i
                if ((iniint != 0) and ((iniint % 10) == 0)):
                    iniint = iniint + 1
                if finint == iniint:
                    iniint = iniint - 1

            link = baseurl + "&range=" + \
                str(iniint) + '-' + str(finint)

            # mostrar erro de ligação no servidor

            r = checkServer(link, loadlink)

            soup = BeautifulSoup(r.text, 'lxml')

            productlist = soup.find_all('span', {"class": "plusSign"})

            # inserir links na array (se não existirem)
            for tag in productlist:
                tagA = tag.find('a')
                link = tagA['href']
                if link not in arraylinks:
                    arraylinks.append(link)

            iniint = iniint + 100

        # processo após o processo anterior estar concluido
        else:
            with open('output.txt', 'w') as filehandle:
                json.dump(arraylinks, filehandle)
            # mostrar estado de conclusao
            if(loadlink != 100):
                loadlink = 100
            print(str(math.trunc(loadlink)) + "%")
            print('Fase 1/2 Concluída')
            # retornar os links
            return arraylinks
