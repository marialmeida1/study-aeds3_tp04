import os
import struct
from tabela_hash import HashExtensivel, RegistroHashExtensivel

# Classe de teste para demonstrar o uso da tabela hash extensível
class TestRecord(RegistroHashExtensivel):
    def __init__(self, key: int = 0, value: str = ""):
        self.key = key
        self.value = value

    def hash_code(self) -> int:
        # Retorna a chave numérica do registro
        return self.key

    def size(self) -> int:
        # Tamanho fixo: 4 bytes para o inteiro e 20 bytes para a string
        return 4 + 20

    def to_byte_array(self) -> bytes:
        # Serializa o registro para bytes
        value_bytes = self.value.encode('utf-8')[:20]
        value_bytes += b' ' * (20 - len(value_bytes))
        return struct.pack('>i', self.key) + value_bytes

    def from_byte_array(self, ba: bytes):
        # Carrega o registro a partir de bytes
        self.key = struct.unpack('>i', ba[:4])[0]
        self.value = ba[4:24].decode('utf-8').rstrip()

    def __str__(self):
        # Representação em string do registro
        return f"({self.key}, '{self.value}')"

# Limpa arquivos de teste antigos, se existirem
cache_dir = os.path.join(os.path.dirname(__file__), '__pycache__')
dir_path = os.path.join(cache_dir, 'test_dir.bin')
buckets_path = os.path.join(cache_dir, 'test_buckets.bin')
if os.path.exists(dir_path):
    os.remove(dir_path)
if os.path.exists(buckets_path):
    os.remove(buckets_path)

# Cria a tabela hash extensível para os testes
hash_table = HashExtensivel(TestRecord, 3, dir_path, buckets_path)

# Testa inserção de registros
print('Testing create:')
for i in range(5):
    rec = TestRecord(i, f"val{i}")
    hash_table.create(rec)
    print(f"Inserted: {rec}")

# Testa leitura dos registros
print('\nTesting read:')
for i in range(5):
    rec = hash_table.read(i)
    print(f"Read key {i}: {rec}")

# Testa atualização de um registro
print('\nTesting update:')
rec = TestRecord(2, "updated")
updated = hash_table.update(rec)
print(f"Update key 2: {updated}")
print(f"Read key 2 after update: {hash_table.read(2)}")

# Testa remoção de um registro
print('\nTesting delete:')
deleted = hash_table.delete(3)
print(f"Delete key 3: {deleted}")
print(f"Read key 3 after delete: {hash_table.read(3)}")

# Testa impressão do diretório e dos cestos
print('\nTesting print:')
hash_table.print()
