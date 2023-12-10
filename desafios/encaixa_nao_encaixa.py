''' 
Desafio

Paulinho tem em suas mãos um novo problema. 
Agora a sua professora lhe pediu que construísse um programa para verificar, 
à partir de dois valores muito grandes A e B, se B corresponde aos últimos dígitos de A.

Entrada

A entrada consiste de vários casos de teste. 
A primeira linha de entrada contém um inteiro N que indica a quantidade de casos de teste. 
Cada caso de teste consiste de dois valores A e B maiores que zero, 
cada um deles podendo ter até 1000 dígitos.

Para cada caso de entrada imprima uma mensagem indicando se o segundo valor encaixa no primeiro valor.
'''
N = int(input())

while(N > 0):
    N-=1
    numbers = input()
    splited_numbers = numbers.split()
    number_A_length = len(splited_numbers[0])
    number_B_length = len(splited_numbers[1])
    if number_A_length <= 1000 and number_B_length <= 1000:
      length_difference = number_A_length - number_B_length
      if splited_numbers[0][length_difference:] == splited_numbers[1]:
        print('encaixa')
      else:
        print('nao encaixa')