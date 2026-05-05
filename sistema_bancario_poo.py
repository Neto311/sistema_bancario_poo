from abc import ABC, abstractmethod
from datetime import datetime, strftime, date, time
from pathlib import Path 

PATH = Path("/Users/osvaldocelottineto/Documents/sistema_bancario_poo/").parent()



def log(funcao):
    def envelope(*args, **kwargs):
        resultado = funcao(*args, **kwargs)
        agora = datetime.now()
        data_formatada = agora.strftime('%d/%m/%Y')

        with open(PATH / "log.txt", 'a', encoding = "utf-8") as arq:
            arq.write(f"""[{data_formatada}], Função: {funcao.__name__.upper()} executada com: {args} e {kwargs}
                      com o valor retornado: {resultado}
                      """)
        
        return resultado
    
    return envelope


class Cliente:
    def __init__(self, endereço):
        self._endereço = endereço
        self._contas = []
    
    def realizar_transação(self, conta, transacao):
        if len(conta.historico.transacoes_hoje()) > 10:
            print ("Limite de transações diário atingido")
            return
        else:
            transacao.registrar(conta)
            return 
    
    def adcionar_conta (self):
        self._contas.append()

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_de_nascimento, **kw):
        super().__init__(**kw)
        self.nome = nome
        self.cpf = cpf
        self.data_de_nascimento = data_de_nascimento

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.cpf}')>"



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
    @log
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        if valor > self._saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        
        if valor > 0:
            self._saldo -= valor
            return True
        
        print("Operação falhou! Valor de saque inválido.")
        return False
    
    def depositar (self, valor):
        if valor > 0 :
            self._saldo += valor
            return True
        else:
            print("Operação falhou! Valor de depósito inválido.")
            return False
        

class ContaCorrente(Conta):
    def __init__ (self, numero, cliente, limite = 500, limite_saques = 12):
        self.limite = limite
        self.limite_saque = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print ("Valor acima do seu limite")
        
        elif excedeu_saques:
            print("Excedeu limite de saques diário")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}"""

        
class Historico:
    def __init__(self):
        self._transacao = []
    
    @property
    def transacoes(self):
        return self._transacao
    
    def adicionar_transacao (self, transacao):
        self._transacao.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )
    
    def gerar_relatorio(self, tipo_transacao):
        for transacao in self._transacao:
            if (tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower()):
                yield transacao 
    
    def transacoes_hoje(self):
        transacoes = []
        for transacao in self._transacao:
            data_transacao = datetime.strptime(transacao["data"], "%d/%m/%Y %H:%M:%S").date()
            if data_transacao == date.today():
                transacoes.append(transacao)
        return transacoes




class Transacao(ABC):
    @property
    @classmethod
    @abstractmethod
    def valor(self):
        pass

    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__ (self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    @log
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
    
    @log
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



class MeuIterador():
    def __init__(self, contas):
        self.contas = contas
        self._index = 0


    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            dados = {
                'numero': conta.numero,
                'agencia': conta.agencia,
                'saldo': conta.saldo,
                'cliente': conta.cliente.nome
            }
            self._index += 1 
            return f'A conta é: {conta.numero} e os dados dela são: {dados}'
        except IndexError:
            raise StopIteration
        

