from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereço):
        self._endereço = endereço
        self._contas = []
    
    def realizar_transação(self, conta, transacao):
        transacao.registrar(conta)
    
    def adcionar_conta (self):
        self._contas.append()

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_de_nascimento, **kw):
        super().__init__(**kw)
        self.nome = nome
        self.cpf = cpf
        self.data_de_nascimento = data_de_nascimento



class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, saque):
        self.saque = saque
        if self.saque < self.saldo:
            return "Valor sacado"
        else:
            return "Valor indisponível para saque"
    
    def depositar (self, valor):
        if valor > 0 :
            self._saldo += valor
        
        else:
            return "Valor deve ser maior que 0"
        

class ContaCorrente(Conta):
    def __init__ (self, numero, cliente, limite = 500, limite_saques = 12):
        self.limite = limite
        self.limite_saque = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.Historico.transacoes if transacao ["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print ("Valor acima do seu limite")
        
        elif excedeu_saques:
            print("Excedeu limite de saques diário")
        
        else:
            return super().sacar(valor)

        
class Historico:
    def __init__(self, transacao):
        self._transacao = []
    
    @property
    def transacoes(self):
        return self._transacao
    
    def adicionar_transcao (self, transacao):
        self._transacao.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor
            }
        )


class Transacao(ABC):
    @property
    @classmethod
    @abstractmethod
    def sacar(self):
        pass

    def registar(self):
        pass


class Saque(Transacao):
    def __init__ (self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.append(self)

class Depoisto(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def regsitrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.historico.append(self)