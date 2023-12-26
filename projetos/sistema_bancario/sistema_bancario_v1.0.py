#!/usr/bin/env python3
# -*- coding: utf-8 -*-

titulo = 'Banco dos Devs'
menu = '''

    Menu de Acoes:
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    
'''

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

while (True):
    print('\n')
    print(titulo.center(30, '-'))
    print(menu)
    opcao = input('Escolha uma opcao: ')
    
    if opcao == 'd':
        print('\n')
        print(('Deposito').center(30, '-'))
        deposito = float(input('\nDigite o valor do deposito: '))
        if deposito > 0:
            saldo += deposito
            extrato += f'\nDeposito: R$ {deposito:.2f}\n'
            print('\nDeposito realizado com sucesso!\n')
        else:
            print('\nValor negativo, nao foi possivel realizar o deposito...\n')
    
    elif opcao == 's':
        print('\n')
        print(('Saque').center(30, '-'))
        if numero_saques < LIMITE_SAQUES:
            saque = float(input('\nDigite o valor do saque: '))
            if saque < 0:
                print('\nNao e possivel sacar com valores negativos!')
            elif saque < saldo and saque > 0:
                saldo -= saque
                extrato += f'\nSaque: R$ {saque:.2f}'
                numero_saques+=1
                print('\nSaque realizado com sucesso!')
            else:
                print('\nSaldo insulficiente!') 
        else:
            print('\nLimite de saques diarios atingidos!')
            
    elif opcao == 'e':
        print('\n')
        print(('Extrato').center(30, '-'))
        print('\nNao foram realizadas transacoes.' if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}\n')
        print(30 * '-')
        
    elif opcao == 'q':
        print('\n')
        print(('Saindo...').center(30, '-'))
    
    else:
        print('\nOperacao invalida, selecione a opcao novamente!')