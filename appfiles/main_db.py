# imports
import requests
import sqlite3
from bs4 import BeautifulSoup
from lib.RepresentsInt import RepresentsInt
from data_read import readdata, loadlink
from data_to_xml import loadxml, outXml


def dataColl():  # funcao para colheita de dados (a ser alterado)

    # verificar numero de resultados do link (a ser removido, falta teste de conexao)
    baseurl = 'http://www.base.gov.pt/Base/pt/ResultadosPesquisa?type=contratos&query=atedatapublicacao%3D2020-07-08'
    check = requests.get(baseurl)
    num = BeautifulSoup(check.text, 'lxml')
    checkempty = num.find('span', {"class": "defaultColor strong"})

    # verificar erros de formato do input e dos resultados do link (a ser removido)
    if int(checkempty.text) == 0:
        print("A pesquisa não obteve nenhum resultado.")
    else:
        print(f"Quantidade de contratos (Máximo - {checkempty.text}):")
        contratos = input()
        while RepresentsInt(contratos) == False or int(contratos) < 1 or int(contratos) > int(checkempty.text):
            if (RepresentsInt(contratos) == False):
                print("Deve inserir um número válido.")
                print(f"Quantidade de contratos (Máximo - {checkempty.text}):")
                contratos = input()
            elif int(contratos) < 1:
                print("Deve inserir um número maior que 0.")
                print(f"Quantidade de contratos (Máximo - {checkempty.text}):")
                contratos = input()
            else:
                print(
                    "Deve inserir um número inferior ao número de resultados da pesquisa.")
                print(f"Quantidade de contratos (Máximo - {checkempty.text}):")
                contratos = input()
        else:
            # recolha dos dados para a base de dados
            readdata(baseurl, contratos, checkempty)

            # teste para criacao de xml (a ser removido)
            # outXml("SELECT * FROM 'default'")


dataColl()  # funcao a executar a clicar no botao (a ser removido)
