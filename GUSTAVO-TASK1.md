# Tarefa 1 - Tabela Hash Extensível (AEDs III)

## O que foi feito

Implementei uma Tabela Hash Extensível em Python, baseada no código Java fornecido pelo professor, para ser utilizada em trabalhos acadêmicos da disciplina de Estruturas de Dados III. O projeto foi dividido em dois arquivos principais:

- `tabela_hash.py`: Implementação da estrutura de dados e suas operações.
- `test_tabela_hash.py`: Script de teste para validar todas as funcionalidades da tabela hash extensível.

Os arquivos binários de diretório e cestos são salvos dentro da pasta `__pycache__` para organização.

## Como funciona o código

### 1. Estrutura dos arquivos

- **tabela_hash.py**
  - Define a classe abstrata `RegistroHashExtensivel`, que deve ser herdada por qualquer registro a ser salvo na tabela.
  - Implementa a classe `HashExtensivel`, que possui métodos para criar, ler, atualizar e deletar registros.
  - Possui classes internas:
    - `Cesto`: representa um bucket, armazena registros e controla a profundidade local.
    - `Diretorio`: controla os endereços dos cestos e a profundidade global.
  - Toda a lógica de manipulação de arquivos binários, serialização e gerenciamento de colisões está implementada conforme o modelo Java.

- **test_tabela_hash.py**
  - Define a classe de teste `TestRecord`, que implementa a interface de registro.
  - Realiza testes de inserção, leitura, atualização, remoção e impressão do estado da tabela.
  - Os arquivos binários de teste são criados e removidos automaticamente na pasta `__pycache__`.

### 2. Como usar

1. **Implemente sua classe de registro** herdando de `RegistroHashExtensivel` e definindo os métodos obrigatórios.
2. **Crie uma instância de `HashExtensivel`** passando sua classe, o número máximo de registros por cesto e os caminhos dos arquivos binários (recomenda-se usar a pasta `__pycache__`).
3. **Utilize os métodos** `create`, `read`, `update`, `delete` e `print` para manipular os registros.

### 3. Exemplo de uso

```python
from tabela_hash import HashExtensivel, RegistroHashExtensivel

class MeuRegistro(RegistroHashExtensivel):
    ... # implemente os métodos obrigatórios

hash_table = HashExtensivel(MeuRegistro, 3, '__pycache__/meu_dir.bin', '__pycache__/meu_buckets.bin')
registro = MeuRegistro(1, 'valor')
hash_table.create(registro)
print(hash_table.read(1))
```

### 4. Observações

- O código está todo comentado em português para facilitar o entendimento de outros alunos.
- Os arquivos binários são manipulados diretamente, então é importante garantir que o registro tenha tamanho fixo.
- O diretório e os cestos são duplicados automaticamente conforme a necessidade, seguindo o princípio da hash extensível.

---
