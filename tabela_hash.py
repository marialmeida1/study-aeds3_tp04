import os
import struct
from abc import ABC, abstractmethod
from typing import List, Type, TypeVar, Generic

T = TypeVar('T', bound='RegistroHashExtensivel')

# Classe base abstrata para registros que podem ser usados na tabela hash extensível
# Deve ser herdada por qualquer classe de registro que será armazenada na tabela
class RegistroHashExtensivel(ABC):
    @abstractmethod
    def hash_code(self) -> int:
        # Retorna a chave numérica do registro
        pass

    @abstractmethod
    def size(self) -> int:
        # Retorna o tamanho fixo do registro em bytes
        pass

    @abstractmethod
    def to_byte_array(self) -> bytes:
        # Serializa o registro para um array de bytes
        pass

    @abstractmethod
    def from_byte_array(self, ba: bytes):
        # Carrega o registro a partir de um array de bytes
        pass

# Implementação da Tabela Hash Extensível
# Permite criar, ler, atualizar e deletar registros de tamanho fixo em arquivos binários
class HashExtensivel(Generic[T]):
    class Cesto:
        # Cesto (bucket) armazena os registros e controla a profundidade local
        def __init__(self, cls: Type[T], qtdmax: int, pl: int = 0):
            if qtdmax > 32767:
                raise Exception("Quantidade máxima de 32.767 elementos")
            if pl > 127:
                raise Exception("Profundidade local máxima de 127 bits")
            self.cls = cls
            self.profundidade_local = pl
            self.quantidade = 0
            self.quantidade_maxima = qtdmax
            self.elementos: List[T] = []
            self.bytes_por_elemento = cls().size()
            self.bytes_por_cesto = self.bytes_por_elemento * self.quantidade_maxima + 3

        def to_byte_array(self) -> bytes:
            # Serializa o cesto para bytes
            ba = bytearray()
            ba.append(self.profundidade_local)
            ba += struct.pack('>h', self.quantidade)
            i = 0
            while i < self.quantidade:
                ba += self.elementos[i].to_byte_array()
                i += 1
            vazio = bytes(self.bytes_por_elemento)
            while i < self.quantidade_maxima:
                ba += vazio
                i += 1
            return bytes(ba)

        def from_byte_array(self, ba: bytes):
            # Carrega o cesto a partir de bytes
            self.profundidade_local = ba[0]
            self.quantidade = struct.unpack('>h', ba[1:3])[0]
            self.elementos = []
            offset = 3
            for i in range(self.quantidade_maxima):
                dados = ba[offset:offset+self.bytes_por_elemento]
                elem = self.cls()
                elem.from_byte_array(dados)
                self.elementos.append(elem)
                offset += self.bytes_por_elemento

        def create(self, elem: T) -> bool:
            # Insere um elemento ordenadamente no cesto
            if self.full():
                return False
            i = self.quantidade - 1
            while i >= 0 and elem.hash_code() < self.elementos[i].hash_code():
                i -= 1
            self.elementos.insert(i+1, elem)
            self.quantidade += 1
            return True

        def read(self, chave: int):
            # Busca um elemento pela chave
            if self.empty():
                return None
            i = 0
            while i < self.quantidade and chave > self.elementos[i].hash_code():
                i += 1
            if i < self.quantidade and chave == self.elementos[i].hash_code():
                return self.elementos[i]
            return None

        def update(self, elem: T) -> bool:
            # Atualiza um elemento existente
            if self.empty():
                return False
            i = 0
            while i < self.quantidade and elem.hash_code() > self.elementos[i].hash_code():
                i += 1
            if i < self.quantidade and elem.hash_code() == self.elementos[i].hash_code():
                self.elementos[i] = elem
                return True
            return False

        def delete(self, chave: int) -> bool:
            # Remove um elemento pela chave
            if self.empty():
                return False
            i = 0
            while i < self.quantidade and chave > self.elementos[i].hash_code():
                i += 1
            if i < self.quantidade and chave == self.elementos[i].hash_code():
                self.elementos.pop(i)
                self.quantidade -= 1
                return True
            return False

        def empty(self):
            # Verifica se o cesto está vazio
            return self.quantidade == 0

        def full(self):
            # Verifica se o cesto está cheio
            return self.quantidade == self.quantidade_maxima

        def size(self):
            # Retorna o tamanho do cesto em bytes
            return self.bytes_por_cesto

        def __str__(self):
            # Retorna uma string representando o cesto
            s = f"Profundidade Local: {self.profundidade_local}\nQuantidade: {self.quantidade}\n| "
            for i in range(self.quantidade):
                s += str(self.elementos[i]) + " | "
            for i in range(self.quantidade, self.quantidade_maxima):
                s += "- | "
            return s

    class Diretorio:
        # Diretório controla os endereços dos cestos e a profundidade global
        def __init__(self):
            self.profundidade_global = 0
            self.enderecos = [0]

        def atualiza_endereco(self, p, e):
            # Atualiza o endereço de um cesto no diretório
            if p >= 2 ** self.profundidade_global:
                return False
            self.enderecos[p] = e
            return True

        def to_byte_array(self) -> bytes:
            # Serializa o diretório para bytes
            ba = bytearray()
            ba.append(self.profundidade_global)
            quantidade = 2 ** self.profundidade_global
            for i in range(quantidade):
                ba += struct.pack('>q', self.enderecos[i])
            return bytes(ba)

        def from_byte_array(self, ba: bytes):
            # Carrega o diretório a partir de bytes
            self.profundidade_global = ba[0]
            quantidade = 2 ** self.profundidade_global
            self.enderecos = []
            offset = 1
            for i in range(quantidade):
                endereco = struct.unpack('>q', ba[offset:offset+8])[0]
                self.enderecos.append(endereco)
                offset += 8

        def __str__(self):
            # Retorna uma string representando o diretório
            s = f"\nProfundidade global: {self.profundidade_global}"
            quantidade = 2 ** self.profundidade_global
            for i in range(quantidade):
                s += f"\n{i}: {self.enderecos[i]}"
            return s

        def endereco(self, p):
            # Retorna o endereço do cesto correspondente
            if p >= 2 ** self.profundidade_global:
                return -1
            return self.enderecos[p]

        def duplica(self):
            # Duplica o diretório quando necessário
            if self.profundidade_global == 127:
                return False
            self.profundidade_global += 1
            q1 = 2 ** (self.profundidade_global - 1)
            q2 = 2 ** self.profundidade_global
            novos_enderecos = [0] * q2
            for i in range(q1):
                novos_enderecos[i] = self.enderecos[i]
            for i in range(q1, q2):
                novos_enderecos[i] = self.enderecos[i - q1]
            self.enderecos = novos_enderecos
            return True

        def hash(self, chave):
            # Calcula o índice do diretório para uma chave
            return abs(chave) % (2 ** self.profundidade_global)

        def hash2(self, chave, pl):
            # Calcula o índice para uma profundidade local
            return abs(chave) % (2 ** pl)

    def __init__(self, cls: Type[T], n: int, nd: str, nc: str):
        # Inicializa a tabela hash extensível, criando arquivos se necessário
        self.cls = cls
        self.quantidade_dados_por_cesto = n
        self.nome_arquivo_diretorio = nd
        self.nome_arquivo_cestos = nc
        self.arq_diretorio = open(self.nome_arquivo_diretorio, 'r+b') if os.path.exists(self.nome_arquivo_diretorio) else open(self.nome_arquivo_diretorio, 'w+b')
        self.arq_cestos = open(self.nome_arquivo_cestos, 'r+b') if os.path.exists(self.nome_arquivo_cestos) else open(self.nome_arquivo_cestos, 'w+b')
        if os.path.getsize(self.nome_arquivo_diretorio) == 0 or os.path.getsize(self.nome_arquivo_cestos) == 0:
            self.diretorio = self.Diretorio()
            bd = self.diretorio.to_byte_array()
            self.arq_diretorio.write(bd)
            c = self.Cesto(self.cls, self.quantidade_dados_por_cesto)
            bd = c.to_byte_array()
            self.arq_cestos.seek(0)
            self.arq_cestos.write(bd)

    def create(self, elem: T) -> bool:
        # Insere um novo registro na tabela
        self.arq_diretorio.seek(0)
        bd = self.arq_diretorio.read()
        self.diretorio = self.Diretorio()
        self.diretorio.from_byte_array(bd)
        i = self.diretorio.hash(elem.hash_code())
        endereco_cesto = self.diretorio.endereco(i)
        c = self.Cesto(self.cls, self.quantidade_dados_por_cesto)
        self.arq_cestos.seek(endereco_cesto)
        ba = self.arq_cestos.read(c.size())
        c.from_byte_array(ba)
        if c.read(elem.hash_code()) is not None:
            raise Exception("Elemento já existe")
        if not c.full():
            c.create(elem)
            self.arq_cestos.seek(endereco_cesto)
            self.arq_cestos.write(c.to_byte_array())
            return True
        pl = c.profundidade_local
        if pl >= self.diretorio.profundidade_global:
            self.diretorio.duplica()
        pg = self.diretorio.profundidade_global
        c1 = self.Cesto(self.cls, self.quantidade_dados_por_cesto, pl + 1)
        self.arq_cestos.seek(endereco_cesto)
        self.arq_cestos.write(c1.to_byte_array())
        c2 = self.Cesto(self.cls, self.quantidade_dados_por_cesto, pl + 1)
        self.arq_cestos.seek(0, 2)
        novo_endereco = self.arq_cestos.tell()
        self.arq_cestos.write(c2.to_byte_array())
        inicio = self.diretorio.hash2(elem.hash_code(), c.profundidade_local)
        deslocamento = 2 ** pl
        maximo = 2 ** pg
        troca = False
        for j in range(inicio, maximo, deslocamento):
            if troca:
                self.diretorio.atualiza_endereco(j, novo_endereco)
            troca = not troca
        bd = self.diretorio.to_byte_array()
        self.arq_diretorio.seek(0)
        self.arq_diretorio.write(bd)
        for j in range(c.quantidade):
            self.create(c.elementos[j])
        self.create(elem)
        return True

    def read(self, chave: int):
        # Lê um registro pela chave
        self.arq_diretorio.seek(0)
        bd = self.arq_diretorio.read()
        self.diretorio = self.Diretorio()
        self.diretorio.from_byte_array(bd)
        i = self.diretorio.hash(chave)
        endereco_cesto = self.diretorio.endereco(i)
        c = self.Cesto(self.cls, self.quantidade_dados_por_cesto)
        self.arq_cestos.seek(endereco_cesto)
        ba = self.arq_cestos.read(c.size())
        c.from_byte_array(ba)
        return c.read(chave)

    def update(self, elem: T) -> bool:
        # Atualiza um registro existente
        self.arq_diretorio.seek(0)
        bd = self.arq_diretorio.read()
        self.diretorio = self.Diretorio()
        self.diretorio.from_byte_array(bd)
        i = self.diretorio.hash(elem.hash_code())
        endereco_cesto = self.diretorio.endereco(i)
        c = self.Cesto(self.cls, self.quantidade_dados_por_cesto)
        self.arq_cestos.seek(endereco_cesto)
        ba = self.arq_cestos.read(c.size())
        c.from_byte_array(ba)
        if not c.update(elem):
            return False
        self.arq_cestos.seek(endereco_cesto)
        self.arq_cestos.write(c.to_byte_array())
        return True

    def delete(self, chave: int) -> bool:
        # Remove um registro pela chave
        self.arq_diretorio.seek(0)
        bd = self.arq_diretorio.read()
        self.diretorio = self.Diretorio()
        self.diretorio.from_byte_array(bd)
        i = self.diretorio.hash(chave)
        endereco_cesto = self.diretorio.endereco(i)
        c = self.Cesto(self.cls, self.quantidade_dados_por_cesto)
        self.arq_cestos.seek(endereco_cesto)
        ba = self.arq_cestos.read(c.size())
        c.from_byte_array(ba)
        if not c.delete(chave):
            return False
        self.arq_cestos.seek(endereco_cesto)
        self.arq_cestos.write(c.to_byte_array())
        return True

    def print(self):
        # Imprime o estado atual do diretório e dos cestos
        self.arq_diretorio.seek(0)
        bd = self.arq_diretorio.read()
        self.diretorio = self.Diretorio()
        self.diretorio.from_byte_array(bd)
        print("\nDIRETÓRIO ------------------")
        print(self.diretorio)
        print("\nCESTOS ---------------------")
        self.arq_cestos.seek(0)
        while self.arq_cestos.tell() < os.path.getsize(self.nome_arquivo_cestos):
            print(f"Endereço: {self.arq_cestos.tell()}")
            c = self.Cesto(self.cls, self.quantidade_dados_por_cesto)
            ba = self.arq_cestos.read(c.size())
            c.from_byte_array(ba)
            print(c)