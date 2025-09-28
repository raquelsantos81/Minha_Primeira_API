# Minha Primeira API - Cardápio

## Descrição

Esta é uma API desenvolvida com FastAPI para oferecer dados de um cardápio fictício com diferentes pratos, categorias e preços.  
Permite listar todos pratos, buscar por ID ou categoria, filtrar pratos, montar combos diversos com pratos de categorias diferentes, e adicionar novos pratos.  
Também possui um endpoint que lê diretamente do CSV e expõe os primeiros registros para facilitar testes.

---

## Como rodar o projeto

### Pré-requisitos

- Python 3.7 ou superior instalado.
- Recomenda-se usar um ambiente virtual (venv) para isolar dependências.

### Passos

1. Clone ou baixe o projeto no seu computador.

2. Abra um terminal na pasta do projeto.

3. Crie e ative um ambiente virtual:  
   No Windows PowerShell:
python3 -m venv env
source env/bin/activate


4. Crie o arquivo `requirements.txt` na pasta raiz com o conteúdo:


5. Instale as dependências:
pip install -r requirements.txt

6. Certifique-se que o arquivo `dataset_cardapio.csv` está na pasta `dados` (conforme estrutura do projeto).

7. Rode o servidor FastAPI:
uvicorn main:app --reload


8. No navegador, acesse:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

Esta é a documentação interativa (Swagger UI) onde pode testar facilmente todos os endpoints da API.


## Endpoints disponíveis

| Método | Caminho                               | Descrição                                    Parâmetros                           

| GET    | `/`                                 Informações básicas da API                    Nenhum                            
| GET    | `/dados`                            Lista todos os pratos                           Nenhum                            
| GET    | `/dados/id/{item_id}`               Busca um prato por ID                         `item_id` (int, obrigatório)      
| GET    | `/dados/categoria/{categoria}`      Lista pratos da categoria                     `categoria` (str, obrigatório)    
| GET    | `/dados/buscar`                     Busca pratos com filtros opcionais             Query params: `nome`, `categoria`, `limite` 
| POST   | `/dados`                            Adiciona novo prato                            JSON com dados do prato            
| GET    | `/cardapio/combos-diversidade`      Gera combos diversos com pratos de categorias diferentes | Query param: `qtd` (int)         
| GET    | `/primeiros-registros`              Retorna os primeiros 10 registros lidos do CSV | Nenhum                          



## Como testar os endpoints na documentação

1. Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

2. Clique no endpoint desejado para expandir seu formulário de testes.

3. Para endpoints com parâmetros obrigatórios na URL (ex: `/dados/id/{item_id}`), clique em "Try it out", preencha o campo e clique em "Execute".

4. Para endpoints com query params, preencha os filtros (opcional) e execute.

5. Para o endpoint POST `/dados`, clique em "Try it out", insira o JSON do prato e execute.

6. Para o endpoint `/primeiros-registros`, apenas clique em "Try it out" e "Execute" para ver os primeiros registros do CSV.


## Estrutura do projeto

PROJETO 4 RAQUEL SANTOS/
├─ env/                              ← PASTA do ambiente virtual (venv)
├─ Minha_Primeira_API/               ← PASTA do app
│  ├─ __pycache__/                   ← PASTA de cache do Python (pode ignorar)
│  │  └─ main.cpython-311.pyc        ← ARQUIVO de bytecode gerado
│  ├─ dados/                         ← PASTA de dados
│  │  ├─ criar_csv.py                ← ARQUIVO: script que gera o CSV
│  │  └─ dataset_cardapio.csv        ← ARQUIVO: dataset do cardápio
│  ├─ main.py                        ← ARQUIVO: API FastAPI (endpoints)
│  ├─ README.md                      ← ARQUIVO: instruções do projeto
│  └─ requirements.txt               ← ARQUIVO: dependências (pip install -r)
└─ testes_main copy.py               ← ARQUIVO: rascunho/teste fora do app


## Observações

- Os dados adicionados via POST não são persistidos no CSV, permanecem apenas na memória enquanto o servidor está ativo.
- A leitura do CSV para exposição dos primeiros registros é feita diretamente do arquivo.
- O parâmetro `limite` no endpoint `/dados/buscar` limita o número de resultados retornados.
- O endpoint `/cardapio/combos-diversidade` garante diversidade nas categorias e evita repetir pratos.



Autor: Raquel Santos Faria



