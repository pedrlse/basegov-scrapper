# imports
import math
import io
import sqlite3
import time
from datetime import date
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from lib.ElementTree_pretty import prettify
from pathlib import Path

# variaveis globais
loadxml = 0


def outXml(query):  # funcao para importacao dos dados para xml

    # variaveis locais
    i = 0
    global loadxml

    #   localizacao da pasta transferencias
    downloads = str(Path.home() / "Downloads")

    def escrXml(col):  # funcao para organizacao dos dados
        # variaveis locais
        global check
        global detalhe
        global execc

        # "switch case" para os diferentes elementos de cada coluna na base de dados
        if col == 1:
            detalhe = SubElement(cont, 'detalheContrato')
            detalhe.attrib = {'nome': 'Detalhe do Contrato'}
            tagcont = SubElement(detalhe, 'dataPublicação')
            tagcont.attrib = {'nome': 'Data de publicação no BASE'}
            tagcont.text = lin[col]
        elif col == 2:
            tagcont = SubElement(detalhe, 'tipoContrato')
            tagcont.attrib = {'nome': 'Tipo(s) de contrato'}
            tagcont.text = lin[col]
        elif col == 3:
            tagcont = SubElement(detalhe, 'numRegisto')
            tagcont.attrib = {'nome': 'Nº de registo do acordo quadro'}
            tagcont.text = lin[col]
        elif col == 4:
            tagcont = SubElement(detalhe, 'descAcordo')
            tagcont.attrib = {'nome': 'Descrição do acordo quadro'}
            tagcont.text = lin[col]
        elif col == 5:
            tagcont = SubElement(detalhe, 'tipoProcedimento')
            tagcont.attrib = {'nome': 'Tipo de procedimento'}
            tagcont.text = lin[col]
        elif col == 6:
            tagcont = SubElement(detalhe, 'descrição')
            tagcont.attrib = {'nome': 'Descrição'}
            tagcont.text = lin[col]
        elif col == 7:
            tagcont = SubElement(detalhe, 'fundamentação')
            tagcont.attrib = {'nome': 'Fundamentação'}
            tagcont.text = lin[col]
        elif col == 8:
            tagcont = SubElement(detalhe, 'fundamentaçãoNecessidadeRecurso')
            tagcont.attrib = {
                'nome': 'Fundamentação da necessidade de recurso ao ajuste direto (se aplicável)'}
            tagcont.text = lin[col]
        elif col == 9:
            tagcont = SubElement(detalhe, 'entidadeAdjudicante')
            tagcont.attrib = {
                'nome': 'Entidade adjudicante - Nome, NIF'}
            tagcont.text = lin[col]
        elif col == 10:
            tagcont = SubElement(detalhe, 'entidadeAdjudicatária')
            tagcont.attrib = {
                'nome': 'Entidade adjudicatária - Nome, NIF'}
            tagcont.text = lin[col]
        elif col == 11:
            tagcont = SubElement(detalhe, 'objetoContrato')
            tagcont.attrib = {
                'nome': 'Objeto do Contrato'}
            tagcont.text = lin[col]
        elif col == 12:
            tagcont = SubElement(detalhe, 'procedimentoCentralizado')
            tagcont.attrib = {
                'nome': 'Procedimento Centralizado'}
            tagcont.text = lin[col]
        elif col == 13:
            tagcont = SubElement(detalhe, 'cpv')
            tagcont.attrib = {
                'nome': 'CPV'}
            tagcont.text = lin[col]
        elif col == 14:
            tagcont = SubElement(detalhe, 'dataContrato')
            tagcont.attrib = {
                'nome': 'Data de celebração do contrato'}
            tagcont.text = lin[col]
        elif col == 15:
            tagcont = SubElement(detalhe, 'preçoContratual')
            tagcont.attrib = {
                'nome': 'Preço contratual'}
            tagcont.text = lin[col]
        elif col == 16:
            tagcont = SubElement(detalhe, 'prazoExecução')
            tagcont.attrib = {
                'nome': 'Prazo de execução'}
            tagcont.text = lin[col]
        elif col == 17:
            tagcont = SubElement(detalhe, 'localExecução')
            tagcont.attrib = {
                'nome': 'Local de execução - País, Distrito, Concelho'}
            tagcont.text = lin[col]
        elif col == 18:
            tagcont = SubElement(detalhe, 'concorrentes')
            tagcont.attrib = {
                'nome': 'Concorrentes'}
            tagcont.text = lin[col]
        elif col == 19:
            tagcont = SubElement(detalhe, 'anúncio')
            tagcont.attrib = {
                'nome': 'Anúncio'}
            tagcont.text = lin[col]
        elif col == 20:
            tagcont = SubElement(detalhe, 'incrementos')
            tagcont.attrib = {
                'nome': 'Incrementos superiores a 15%'}
            tagcont.text = lin[col]
        elif col == 21:
            tagcont = SubElement(detalhe, 'documentos')
            tagcont.attrib = {
                'nome': 'Documentos'}
            tagcont.text = lin[col]
        elif col == 22:
            tagcont = SubElement(detalhe, 'observações')
            tagcont.attrib = {
                'nome': 'Observações'}
            tagcont.text = lin[col]
        elif col == 23:
            execc = SubElement(cont, 'execuçãoContrato')
            check = 1
            execc.attrib = {'nome': 'Execução do Contrato'}
            tagcont = SubElement(execc, 'dataFecho')
            tagcont.attrib = {
                'nome': 'Data de fecho do contrato'}
            tagcont.text = lin[col]
        elif col == 24:
            if check != 1:
                execc = SubElement(cont, 'execuçãoContrato')
            check = 0
            tagcont = SubElement(execc, 'preçoTotal')
            tagcont.attrib = {
                'nome': 'Preço total efetivo'}
            tagcont.text = lin[col]
        elif col == 25:
            tagcont = SubElement(execc, 'causasAlteraçõesPrazo')
            tagcont.attrib = {
                'nome': 'Causas das alterações ao prazo'}
            tagcont.text = lin[col]
        elif col == 26:
            tagcont = SubElement(execc, 'causasAlteraçõesPreço')
            tagcont.attrib = {
                'nome': 'Causas das alterações ao preço'}
            tagcont.text = lin[col]

    print("A converter para XML...")

    # conexao com a base de dados
    conn = sqlite3.connect('db/default.db')
    c = conn.cursor()

    # leitura de toda a base de dados
    c.execute(query)
    lins = c.fetchall()

    # data atual e formatos
    dia = date.today()
    hora = time.localtime()
    diaformat = dia.strftime("%d-%m-%Y")
    horaformat = time.strftime("%HH%M.%Ss", hora)
    horaformat2 = time.strftime("%H:%M:%S", hora)

    # elemento root do XML
    root = Element('resultadosPesquisa')
    root.set('nome', 'Resultados da Pesquisa efectuada')
    root.append(Comment('Gerado por data-reader'))

    # outros elementos do XML
    head = SubElement(root, 'cabeçalho')
    title = SubElement(head, 'título')
    title.text = 'Dados recolhidos da plataforma Base GOV'
    dc = SubElement(head, 'dataCriação')
    dc.text = str(diaformat) + ' ' + str(horaformat2)
    dm = SubElement(head, 'dataModificação')
    dm.text = str(diaformat) + ' ' + str(horaformat2)
    conts = SubElement(root, 'contratos')

    # obtencao dos dados por cada linha da base de dados
    comp = len(lins)
    for lin in lins:
        # mostrar estado de conclusao
        print(str(math.trunc(loadxml)) + '%')

        loadxml = loadxml + 100/comp
        cont = SubElement(conts, 'contrato')
        while i < len(lin):
            if lin[i] != None and i != 0:
                escrXml(i)
            i = i+1
        else:
            i = 0

    # inserir os dados num ficheiro XML
    xmlfile = io.open(downloads + "/resultado_" + str(diaformat) + '_' +
                      str(horaformat) + '.xml', 'w', encoding="utf-8")
    xmlfile.write(prettify(root))
    xmlfile.close()

    # apagar dados da base de dados e terminar a conexao com a mesma
    c.execute("DELETE FROM 'default' WHERE id > 0")
    conn.commit()
    c.execute("UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='default'")
    conn.commit()
    c.close()

    # mostrar estado de conclusao
    print(str(math.trunc(loadxml)) + '%')
    print("Ficheiro XML disponível na pasta Transferências")
