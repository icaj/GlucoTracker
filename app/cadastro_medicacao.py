from crud.crud_medicacao import inserir_medicacao, buscar_medicacoes_por_paciente, atualizar_medicacao, apagar_medicacao
from crud.crud_paciente import *
from util.util import exibir_medicacoes, menu_padrao, checar_sn, formato_hora, form_padrao, print_wait
import time
from entidades.medicacao import Medicacao

form_medicacao = [
    "Nome da medicacao: ",
    "Dose prescrita: ",
    "Horario diario inicial: ", 
    lambda u: time.strptime(u, formato_hora),
    "Tomar a cada quantas horas: ", int, 
    "Alarmar nesses horarios? [s/n] ", checar_sn,
]

def medicacao_tela(id_pct):
    menu_padrao("Home > Medicacao", [
        "Nova", 
        lambda: medicacao_nova(id_pct),
        "Listar", 
        lambda: medicacao_listar(id_pct),
        "Editar", 
        lambda: medicacao_editar(id_pct),
        "Apagar",
        lambda: medicacao_apagar(id_pct),
    ])

def medicacao_nova(id_pct):
    dados = form_padrao(form_medicacao)
    return inserir_medicacao(id_pct.codigo, dados[0], dados[1], dados[2], dados[3], dados[4])

def medicacao_listar(id_pct, w=True):
    medicacoes = buscar_medicacoes_por_paciente(id_pct.codigo)
    print("Medicações: ")
    exibir_medicacoes(medicacoes)
    if w:
        print_wait()
    return medicacoes

def medicacao_editar(id_pct):
    registros = medicacao_listar(id_pct, w=False)
    cod = input("ID do que deseja editar: ")
    med = filter(lambda r: r.codigo == cod, registros)
    if len(med) > 0:
        med = med[0]
    else:
        print("Nao encontrado!")
        return
    resp = form_padrao(form_medicacao, [
        med.nome, med.dosagem, med.hora_inicial, 
        med.periodicidade, med.lembrar,
    ])
    return atualizar_medicacao(cod, id_pct.codigo, resp[0], resp[1], resp[2], resp[3], resp[4])

def medicacao_apagar(id_pct):
    medicacao_listar(id_pct)
    cod = input("ID do quep deseja apagar: ")
    if cod == "":
        print_wait("Operacao cancelada.")
    elif apagar_medicacao(cod):
        print_wait("Apagado com sucesso.")
    else:
        print_wait("Não encontrado.")
        