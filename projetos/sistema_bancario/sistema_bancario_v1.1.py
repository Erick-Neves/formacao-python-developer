#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textwrap

# Função que exibe o menu de opções
def menu():
    menu = '''\n
    ========== Banco dos Devs ========== 
    Menu de Ações:
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo Usuário
    [q]\tSair
    '''
    return input(textwrap.dedent(menu))

# Função que recebe apenas argumentos posicionais
def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f'Depósito:\tR$ {valor_deposito:.2f}\n'
        print('\n=== Depósito realizado com sucesso! ===\n')
    else:
        print('\nValor negativo, nao foi possivel realizar o deposito...\n')
    return saldo, extrato

# Função que recebe apenas argumentos nomeados
def sacar(*, saldo, valor_saque, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor_saque > saldo
    excedeu_limite = valor_saque > limite
    excedeu_saques = numero_saques > limite_saques
    
    if excedeu_saldo:
        print('\n=== Operação falhou! Você não tem saldo suficiente...')
    
    elif excedeu_limite:
        print('\n=== Operação falhou! O valor do saque excede o limite...')
    
    elif excedeu_saques:
        print('\n=== Operação falhou! Número máximo de saques excedido...')
    
    elif valor_saque > 0:
        saldo -= valor_saque
        extrato += f'Saque:\t\tR$ {valor_saque:.2f}\n'
        numero_saques+=1
        print('\n=== Saque realizado com sucesso! ===')

    else:
        print('\n=== Operação falhou! O valor informado é inválido...')
        
    return saldo, extrato, numero_saques

# Função que recebe um parâmetro posicional e um nomeado
def exibir_extrato(saldo, /, *, extrato):
    print(('Extrato').center(30, '-'))
    print('\nNao foram realizadas transacoes.' if not extrato else extrato)
    print(f'\nSaldo: R$ {saldo:.2f}')
    print(30 * '-')

# Função que filtra se existem usuarios já cadastrados com tal CPF
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"]==cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função que cria um novo usuário
def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print('\n--- Já existe um usuário com este CPF!... ---')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estrado): ')
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    
    print('=== Usuário criado com sucesso! ===')

# Função que cria uma nova conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n=== Usuário não encontrado, fluxo de criação encerrado!... ===")

# Função que lista todas as contas criadas na sessão
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("="*30)
        print(textwrap.dedent(linha))

# Código principal da aplicação
def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001' 
    
    numero_saques = 0
    saldo = 0
    limite = 500
    extrato = ''
    usuarios = []
    contas = []

    while (True):
        opcao = menu()
        
        if opcao == 'd':
            valor_deposito = float(input('Digite o valor do deposito: '))
            saldo, extrato = depositar(saldo, valor_deposito, extrato)
            
        elif opcao == 's':
            valor_saque = float(input('\nDigite o valor do saque: '))
            
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor_saque=valor_saque,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
                
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == 'nu':
            criar_usuario(usuarios)
            
        elif opcao == 'nc':
            numero_conta = len(contas)+1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
            
        elif opcao == 'lc':
            listar_contas(contas)
            
        elif opcao == 'q':
            print('\n')
            print(('Saindo...').center(30, '-'))
        
        else:
            print('\nOperacao invalida, selecione a opcão novamente!')

main()