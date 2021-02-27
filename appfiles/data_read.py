# imports
import requests
import math
import sqlite3
import re
from bs4 import BeautifulSoup
from link_read import readlinks, loadlink, checkServer
import numpy as np
# variaveis globais
loaddata = 0


# funcao para recolher e inserir os dados na base de dados
def readdata(baseurl, contratos, checkempty):

    # conexao com a base de dados
    conn = sqlite3.connect('db/default.db')

    c = conn.cursor()

    # leitura dos links recolhidos
    arraylinks = np.loadtxt("output.txt", comments="#",
                            delimiter=",", unpack=False, dtype=str)

    #arraylinks = readlinks(int(contratos), baseurl, checkempty.text)

    print('A registar na base de dados...')

    # variaveis locais
    i = 0
    global loaddata

    # processo de recolha e insercao de dados na base de dados
    while i < len(arraylinks):
        arraylist = []
        baseurl = arraylinks[i]

        source = checkServer(baseurl, loaddata)

        soup = BeautifulSoup(source.text, 'lxml')

        listadados = soup.find_all('tr')

        for dados in listadados:
            td = dados.find_all("td")[1].text
            td = re.sub('\s+', ' ', td)
            if td in ("-", " - ", "Não aplicável"):
                arraylist.append(None)
            else:
                arraylist.append(td)
        if len(arraylist) > 25:
            c.execute("INSERT INTO 'default'(datapub,tipocont,numreg,descaco,tipoproc,desc,fund,fundajust,adjude,adjuda,objet,proced,cpv,dataceleb,preccont,prazexec,local,conc,anun,incresup,docs,obs,datafecho,prectot,causpraz,causprec, conv) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (arraylist[0], arraylist[1], arraylist[2], arraylist[
                3], arraylist[4], arraylist[5], arraylist[6], arraylist[7], arraylist[8], arraylist[9], arraylist[10], arraylist[11], arraylist[12], arraylist[13], arraylist[14], arraylist[15], arraylist[16], arraylist[17], arraylist[18], arraylist[19], arraylist[20], arraylist[21], arraylist[22], arraylist[23], arraylist[24], arraylist[25], None))
        elif len(arraylist) < 25:
            c.execute("INSERT INTO 'default'(datapub,tipocont,numreg,descaco,tipoproc,desc,fund,fundajust,adjude,adjuda,objet,proced,cpv,dataceleb,preccont,prazexec,local,conc,anun,incresup,docs,obs,datafecho,prectot,causpraz,causprec, conv) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (arraylist[0], arraylist[1], None, None, arraylist[2], arraylist[3], arraylist[4], arraylist[5], arraylist[6], arraylist[7], arraylist[8], arraylist[9], arraylist[10], arraylist[11], arraylist[12], arraylist[13], arraylist[14], arraylist[15], arraylist[16], arraylist[17], arraylist[18], arraylist[19], arraylist[20], arraylist[21], arraylist[22], arraylist[23], None))
        else:
            c.execute("INSERT INTO 'default'(datapub,tipocont,numreg,descaco,tipoproc,desc,fund,fundajust,adjude,adjuda,objet,proced,cpv,dataceleb,preccont,prazexec,local,conc,anun,incresup,docs,obs,datafecho,prectot,causpraz,causprec, conv) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                      (arraylist[0], arraylist[1], None, None, arraylist[2], arraylist[3], arraylist[4], arraylist[5], arraylist[6], arraylist[7], arraylist[8], arraylist[9], arraylist[10], arraylist[11], arraylist[12], arraylist[13], arraylist[14], arraylist[16], arraylist[17], arraylist[18], arraylist[19], arraylist[20], arraylist[21], arraylist[22], arraylist[23], arraylist[24], arraylist[15]))

        conn.commit()

        i = i + 1
        # mostrar estado de conclusao
        print(str(math.trunc(loaddata)) + '%')

        loaddata = loaddata + 100/len(arraylinks)
    else:
        # mostrar estado de conclusao
        print(str(math.trunc(loaddata)) + '%')
        print('Fase 2/2 Concluída')

        # terminar conexao com a base de dados
        conn.close()
