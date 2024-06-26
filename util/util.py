from prettytable import PrettyTable
import pyfiglet
import re
from datetime import date
import os
import json
from entidades.tipo_diabete import TipoDiabete
import datetime

formato_hora = "%H:%M"
formato_data = "%d/%m/%y"

def limpa_tela():
    os.system("cls" if os.name == "nt" else "clear")
    
def nome_sistema():
    titulo = pyfiglet.figlet_format("GlucoTrack")
    print(titulo, "versão 1.0")
    print()

def listar_dados(dicionario):
    tabela = PrettyTable()

    if len(dicionario) == 0:
        tabela.field_names = ["Sem registros ainda!"]
        print(tabela)
        print()
        return

    campos = list(dicionario[0].keys())

    tabela.field_names = campos

    linha = ''
    for dado in dicionario:
        for campo in campos:
            linha = dado[campo]
        tabela.add_row(linha)

    print(tabela)

def exibir_medicacoes(medicacoes):
    tabela = PrettyTable()

    if len(medicacoes) == 0:
        tabela.field_names = ["Sem registros ainda!"]
        print(tabela)
        print()
        return

    campos = ['Código', 'Medicação', 'Dosagem', 'Hora Inicial', 'Periodicidade', 'Lembrar']

    tabela.field_names = campos

    for dado in medicacoes:
        tabela.add_row([dado['codigo'], dado['nome'], dado['dosagem'], dado['hora_inicial'], dado['periodicidade'], 'Sim' if dado['lembrar'] == True else 'Não' ])

    print(tabela)

def validar_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

def descricao_tipo_diabete(codigo):
    arquivo = "dados/tipos_diabetes.json"

    if not os.path.exists(arquivo):
        tipos = [ { "codigo": 1, "descricao": "Tipo 1" },
                  { "codigo": 2, "descricao": "Tipo 2" },
                  { "codigo": 3, "descricao": "Gestacional" },
                  { "codigo": 4, "descricao": "Outros"},
                  { "codigo": 5, "descricao": "Não possui"} ]

        with open(arquivo, 'w') as f:
            json.dump(tipos, f, indent=4)

    with open(arquivo, "r") as f:
        tipos = json.load(f)
    
    for r in tipos:
        if r['codigo'] == codigo:
            return r['descricao']

def descricao_sexo(codigo):
    arquivo = "dados/sexo.json"

    if not os.path.exists(arquivo):
        tipos = [ { "codigo": "F", "descricao": "Feminino" },
                  { "codigo": "M", "descricao": "Masculino" }]

        with open(arquivo, 'w') as f:
            json.dump(tipos, f, indent=4)

    with open(arquivo, "r") as f:
        tipos = json.load(f)
    
    for r in tipos:
        if r['codigo'] == codigo:
            return r['descricao']

def menu_padrao(titulo, opcoes):
    acoes = opcoes[1::2]
    opcoes = opcoes[0::2]
    while True:
        limpa_tela()
        nome_sistema()
        print(f"# {titulo}\n")
        print("Operacoes:\n")
        for i, op in enumerate(opcoes):
            print(f"{i+1}. {op}")
        print("0. Sair\n")
        choice = input("Digite a desejada: ")
        if choice.isdigit():
            choice = int(choice)
        else:
            continue
        if choice == 0 or choice > len(opcoes):
            return
        print()
        if a := acoes[choice-1]:
            a()

def checar_sn(u):
    if u.upper() == 'S' or u.upper() == 'N':
        return u.upper() == 'S'
    return None

def pergunta_sn(msg):
    return pergunta_loop(f"{msg} (S/N) ", checar_sn)

def pergunta_loop(msg, checar):
    if not callable(checar):
        checar = lambda x: x
    while True:
        resp = input(msg)
        resp = checar(resp)
        if resp != None:
            return resp

def print_wait(msg=""):
    if msg:
        print(msg)
    return input("Pressione Enter para continuar...")

def form_padrao(list_msg, list_anterior=None, msg_erro="Entrada invalida..."):
    reg = []
    j = -1 
    for i, m in enumerate(list_msg):
        if type(m) != str:
            continue
        j += 1
        checar = list_msg[i+1] if i+1 < len(list_msg) else None
        if not callable(checar):
            checar = lambda x: x

        u = ''
        while True:
            u = input(m)
            try:
                if u == '' and list_anterior:
                    u = list_anterior[j]
                    break
                u = checar(u)
                if u != None:
                    break
                print(msg_erro)
            except Exception as e: 
                print(e)
                
        reg.append(u)
    return reg
