# Trabalho Prático 04 - Algoritimo e Estrutura de Dados

Este projeto apresenta uma implementação de Tabela Hash Extensível em Python, desenvolvida com base em um modelo em Java, adaptada para fins didáticos na disciplina de Estruturas de Dados III. Além da estrutura de dados, foi criado um visualizador interativo utilizando Streamlit para facilitar a inserção, busca, atualização, remoção e visualização dos dados armazenados.

## Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## Como utilizar

Caso ainda não tenham o pip instalado, é necessário instalá-lo previamente para gerenciar os pacotes Python.

Em seguida, é preciso instalar a biblioteca Streamlit, que é utilizada para criar a interface gráfica da aplicação. Para isso, execute o seguinte comando no terminal:

``` 
pip install streamlit
```

Com a instalação concluída, o aplicativo pode ser executado com o comando:

```
streamlit run app.py
```

Isso abrirá uma interface interativa no navegador, permitindo a manipulação da Tabela Hash Extensível de forma visual e prática.

## Exemplo de uso da interface

Após rodar o comando `streamlit run app.py`, uma interface será aberta no navegador. Nela, é possível:

- Inserir um novo registro informando a chave e os dados;
- Buscar um registro digitando a chave;
- Atualizar um registro existente;
- Remover registros da tabela;
- Visualizar, em tempo real, o estado interno da tabela e o nível de ocupação dos cestos.

## Estrutura do Projeto

O projeto está dividido em dois arquivos principais:

- `tabela_hash.py`: Implementação da estrutura de dados da tabela hash extensível.
- `app.py`: Interface gráfica com Streamlit para interação com a tabela de forma visual.
- `test_tabela_hash.py`: Script de teste para validar todas as funcionalidades da tabela hash extensível.

Os arquivos binários gerados (diretório e cestos) são salvos na pasta `__pycache__` para manter a organização do projeto.

## Funcionamento do Código

- **tabela_hash.py**
    - Define a classe abstrata `RegistroHashExtensivel`, que deve ser herdada por qualquer tipo de registro utilizado na tabela.
    - Implementa a classe HashExtensivel, contendo os métodos essenciais: `create`, `read`, `update` e `delete`.
    - Contém as classes internas:
        - `Cesto`: representa um bucket, controlando os registros e a profundidade local.
        - `Diretorio`: armazena os endereços dos cestos e a profundidade global.
    - Toda a manipulação de arquivos binários, serialização e tratamento de colisões segue o padrão da técnica de hashing extensível.

- **app.py**
    - Interface gráfica construída com `Streamlit`.
    - Permite realizar as seguintes operações:
        - Inserção de novos registros.
        - Leitura de registros pela chave.
        - Atualização de registros existentes.
        - Remoção de registros.
        - Visualização da estrutura do diretório e dos buckets, com cores que indicam o nível de ocupação de cada cesto.

- **test_tabela_hash.py**
  - Define a classe de teste `TestRecord`, que implementa a interface de registro.
  - Realiza testes de inserção, leitura, atualização, remoção e impressão do estado da tabela.
  - Os arquivos binários de teste são criados e removidos automaticamente na pasta `__pycache__`.

### Geração da Tabela Hash

- O código está todo comentado em português para facilitar o entendimento de outros alunos.
- Os arquivos binários são manipulados diretamente, então é importante garantir que o registro tenha tamanho fixo.
- O diretório e os cestos são duplicados automaticamente conforme a necessidade, seguindo o princípio da hash extensível.

### Visualizador de Tabela Hash Extensível com Streamlit

- A visualização dos cestos é feita com cores que indicam o estado:
    - 🟥 **Vermelho**: cesto cheio.
    - 🟨 **Amarelo**: parcialmente ocupado.
    - 🟩 **Verde**: vazio.
- Os arquivos binários são manipulados diretamente, e os registros precisam ter tamanho fixo para garantir o funcionamento correto.
- A estrutura da tabela se adapta automaticamente conforme a necessidade, com duplicação do diretório e divisão dos cestos, conforme preconizado pelo hashing extensível.
- O código foi escrito em português com comentários explicativos, visando facilitar o aprendizado e a compreensão por parte dos estudantes.

## Relato de Experiência

Desenvolver a Tabela Hash Extensível em Python foi uma experiência desafiadora e enriquecedora. Adaptamos a lógica de um código Java para Python, o que exigiu compreensão profunda da manipulação de arquivos binários e do funcionamento interno da estrutura.

A criação de uma interface interativa com Streamlit foi um diferencial importante, pois facilitou a visualização da tabela e ajudou a compreender melhor o comportamento dos cestos e do diretório durante as operações.

O projeto nos permitiu aplicar conceitos teóricos na prática, consolidando o aprendizado da disciplina de Estruturas de Dados III e fortalecendo nossas habilidades com Python e organização de código.

## Resposta ao Checklist

#### A visualização interativa da Tabela Hash Extensível foi criada?
Sim, a visualização foi implementada utilizando a biblioteca Streamlit, permitindo a inserção, leitura, atualização, remoção e visualização gráfica da estrutura da tabela, incluindo os cestos e diretório com indicação de ocupação.

#### Há um vídeo de até 2 minutos demonstrando o uso da visualização?
Sim, foi gravado um vídeo com até 2 minutos demonstrando o uso da interface, apresentando as principais funcionalidades: inserção, leitura, atualização, exclusão de registros e visualização da tabela hash.


#### O trabalho está funcionando corretamente?
Sim, todos os testes foram realizados com sucesso. A tabela hash extensível está funcionando conforme o esperado, tanto via interface Streamlit quanto por meio dos testes automatizados no arquivo test_tabela_hash.py.


#### O trabalho está completo?
Sim, o trabalho contempla a implementação da estrutura de dados, os testes automatizados e a interface gráfica interativa, além de estar bem documentado e organizado.


#### O trabalho é original e não a cópia de um trabalho de um colega?
Sim, o trabalho é original. Foi desenvolvido com base no código Java fornecido pelo professor, mas toda a implementação em Python, incluindo a interface com Streamlit, foi feita pelos integrantes do grupo de forma independente.

## Licença

Este projeto foi desenvolvido com fins acadêmicos e pode ser utilizado por estudantes para fins educacionais.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests* para melhorias.
