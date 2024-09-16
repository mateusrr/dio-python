from abc import ABC, abstractmethod
from datetime import date

# Classe abstrata Transacao
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# Classe Historico que armazena as transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Classe abstrata Conta
class Conta:
    def __init__(self, cliente, numero, agencia):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        else:
            print("Saldo insuficiente ou valor inválido.")
            return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(f"Depósito de R$ {valor:.2f}")
            return True
        else:
            print("Valor de depósito inválido.")
            return False

# Classe ContaCorrente que herda de Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Número máximo de saques atingido.")
            return False
        if valor > self.limite:
            print(f"Valor excede o limite de saque de R$ {self.limite:.2f}")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False

# Classes de Transação (Depósito e Saque)
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

# Classe Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe PessoaFisica que herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Função para criar uma nova conta corrente
def criar_conta_corrente(cliente):
    numero = int(input("Digite o número da conta: "))
    agencia = input("Digite o número da agência: ")
    limite = float(input("Digite o limite de saque: "))
    limite_saques = int(input("Digite o limite de quantidade de saques: "))
    return ContaCorrente(cliente=cliente, numero=numero, agencia=agencia, limite=limite, limite_saques=limite_saques)

# Função para criar um cliente
def criar_cliente():
    cpf = input("Digite o CPF: ")
    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (AAAA-MM-DD): ")
    ano, mes, dia = map(int, data_nascimento.split('-'))
    endereco = input("Digite o endereço: ")
    return PessoaFisica(cpf=cpf, nome=nome, data_nascimento=date(ano, mes, dia), endereco=endereco)

# Função para realizar operações na conta
def realizar_operacao(cliente, conta):
    while True:
        print("\nEscolha a operação:")
        print("1. Depósito")
        print("2. Saque")
        print("3. Mostrar saldo")
        print("4. Mostrar histórico")
        print("5. Sair")
        opcao = int(input("Opção: "))

        if opcao == 1:
            valor = float(input("Digite o valor do depósito: "))
            cliente.realizar_transacao(conta, Deposito(valor))
        elif opcao == 2:
            valor = float(input("Digite o valor do saque: "))
            cliente.realizar_transacao(conta, Saque(valor))
        elif opcao == 3:
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
        elif opcao == 4:
            print("Histórico de transações:")
            for transacao in conta.historico.transacoes:
                print(transacao)
        elif opcao == 5:
            break
        else:
            print("Opção inválida, tente novamente.")

# Exemplo de uso interativo
if __name__ == "__main__":
    print("Bem-vindo ao Sistema Bancário!")

    # Criando um cliente
    cliente = criar_cliente()

    # Criando uma conta corrente para o cliente
    conta = criar_conta_corrente(cliente)

    # Adicionando conta ao cliente
    cliente.adicionar_conta(conta)

    # Realizando operações na conta
    realizar_operacao(cliente, conta)
