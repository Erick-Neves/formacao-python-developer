#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textwrap

from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor_saque):
        
        saldo_disponivel = self.saldo
        excedeu_saldo = valor_saque > saldo_disponivel
        
        if excedeu_saldo:
            print('\n=== Operação falhou! Você não tem saldo suficiente...')
        
        elif valor_saque > 0:
            self._saldo -= valor_saque
            print('\n=== Saque realizado com sucesso! ===')
            return True

        else:
            print('\n=== Operação falhou! O valor informado é inválido...')
            
        return False
    
    def depositar(self, valor_deposito):
        if valor_deposito > 0:
            self._saldo += valor_deposito
            print('\n=== Depósito realizado com sucesso! ===\n')

        else:
            print('\nValor inválido, nao foi possivel realizar o deposito...\n')
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
         super().__init__(numero, cliente)
         self.limite = limite
         self.limite_saques = limite_saques
         
    def sacar(self, valor_saque):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == "Saque"]
        )
        
        excedeu_limite = valor_saque > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print('\n=== Operação falhou! O valor do saque excede o limite...')
        
        elif excedeu_saques:
            print('\n=== Operação falhou! Número máximo de saques excedido...')
        
        else:
            return super().sacar(valor_saque)
        
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
    
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
        else:
            print("=== Não foi possivel realizar o deposito... ===")

# Função que exibe o extrato
def exibir_extrato(clientes):
    cpf = input('Digite o CPF: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("=== Cliente não encontrado...")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(('Extrato').center(30, '-'))
    
    extrato = ""
    transacoes = conta.historico.transacoes
    if not transacoes:
        extrato = "=== Não foram feitas transações... ==="
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print(30 * '-')

def depositar(clientes):
    cpf = input('Digite o CPF: ')
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("=== Cliente não encontrado...")
        return
    
    valor_deposito = float(input('Digite o valor do deposito: '))
    transacao = Deposito(valor_deposito)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input('Digite o CPF: ')
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("=== Cliente não encontrado...")
        return
    
    valor_saque = float(input('Digite o valor do saque: '))
    transacao = Saque(valor_saque)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
# Função que exibe o menu de opções
def menu():
    menu = '''\n
    ========== Banco dos Devs ========== 
    Menu de Ações:
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nu]\tNovo cliente
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    '''
    return input(textwrap.dedent(menu))

# Função que filtra se existem usuarios já cadastrados com tal CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf==cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função que recupera a primeira conta do cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("=== Não existem contas vinculadas a este cliente! ...")
        return
    
    return cliente.contas[0]

# Função que cria um novo usuário
def criar_cliente(clientes):
    cpf = input('Digite o CPF(somente numeros): ')
    
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print('\n--- Já existe um cliente com este CPF!... ---')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estrado): ')
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print('=== Cliente criado com sucesso! ===')

# Função que cria uma nova conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input('Digite o CPF: ')
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("=== Cliente não encontrado...")
        return
    
    conta = ContaCorrente.nova_conta(numero_conta, cliente)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")
    
# Função que lista todas as contas criadas na sessão
def listar_contas(contas):
    for conta in contas:
        print("="*30)
        print(textwrap.dedent(str(conta)))

# Código principal da aplicação
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == 'd':
            depositar(clientes)
            
        elif opcao == 's':
            sacar(clientes)
                
        elif opcao == 'e':
            exibir_extrato(clientes)
        
        elif opcao == 'nu':
            criar_cliente(clientes)
            
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao == 'lc':
            listar_contas(contas)
            
        elif opcao == 'q':
            print('\n')
            print(('Saindo...').center(30, '-'))
        
        else:
            print('\nOperacao invalida, selecione a opcão novamente!')

main()