# TESTE 1 -- início 
from fastapi import FastAPI, HTTPException, Query  
from pydantic import BaseModel  
from typing import List, Dict, Any  
from pathlib import Path  
import csv  

# Inicializa a aplicação FastAPI
app = FastAPI(title="Minha API de Cardápio", version="1.0")

# Modelo Pydantic para um prato do cardápio
class Prato(BaseModel):
    id: int
    nome: str
    preco: float
    categoria: str

# Função para ler os dados do CSV de cardápio
def carregar_cardapio() -> List[Dict[str, Any]]:
    caminho = Path(__file__).parent / "dados" / "dataset_cardapio.csv"
    
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado em {caminho}")
    
    itens = []
    with caminho.open("r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            itens.append({
                "id": int(row["id"]),
                "nome": row["nome"],
                "preco": float(row["preco"]),
                "categoria": row["categoria"]
            })
    return itens

# Carrega os dados ao iniciar
try:
    dados_cardapio = carregar_cardapio()
except FileNotFoundError as e:
    print(e)
    dados_cardapio = []



# TESTE 2 -- primeiros ajustes e desenvolvimento
# Endpoint raiz que retorna informações da API
@app.get("/", tags=["Informações"])
def home():
    return {
        "projeto": "Minha Primeira API",
        "autor": "Raquel Santos Faria",
        "descricao": "API para servir dados do cardápio",
        "total_registros": len(dados_cardapio)
    }

# Retorna todos os pratos
@app.get("/dados", response_model=List[Prato], tags=["Dados"])
def listar_todos():
    return dados_cardapio

# Busca prato por ID
@app.get("/dados/id/{item_id}", response_model=Prato, tags=["Dados"])
def buscar_por_id(item_id: int):
    for item in dados_cardapio:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item com ID {item_id} não encontrado")

# Busca pratos por categoria (case insensitive)
@app.get("/dados/categoria/{categoria}", response_model=List[Prato], tags=["Dados"])
def buscar_por_categoria(categoria: str):
    return [item for item in dados_cardapio if item["categoria"].lower() == categoria.lower()]

# Busca com filtros por nome e categoria, com limite de resultados
@app.get("/dados/buscar", tags=["Dados"])
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 5):
    resultados = dados_cardapio
    if nome:
        resultados = [item for item in resultados if nome.lower() in item["nome"].lower()]
    if categoria:
        resultados = [item for item in resultados if item["categoria"].lower() == categoria.lower()]
    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},
        "resultados": resultados[:limite],
        "total": len(resultados),
    }





# TESTE 3 
from fastapi import FastAPI
import pandas as pd
import json

app = FastAPI()

dados_cardapio = [
    {"id": i, "nome": f"Prato {i}", "preco": round(10 + i * 0.5, 2), 
     "categoria": "Pizza" if i % 3 == 0 else "Lanches" if i % 3 == 1 else "Saladas"}
  for i in range(1, 51)
]
try:
    df_cardapio = pd.DataFrame(dados_cardapio)
except Exception as e:
    print("Erro ao carregar os dados", e)


@app.get("/")
def home():
  
    return {
        "projeto": "Minha API de Cardápio",
        "autor": "Raquel Santos",
        "descricao": "API para servir dados do cardápio",
        "total_registros": len(dados_cardapio)
    }

@app.get("/dados")
def listar_todos():
  

# Opção A: Busca por ID
@app.get("/dados/{item_id}")
def buscar_por_id(item_id: int):
    
 resultado = [item for item in dados_cardapio if item["id"] == item_id]
    if len(resultado) == 0:
        return {"erro": "Item não encontrado"}
    return resultado[0]

# Opção B: Busca por categoria (exemplo alternativo)
@app.get("/categoria/{categoria}")
def buscar_por_categoria(categ: str):
    
   filtred = [x for x in dados_cardapio if x["categoria"].lower() == categ.lower()]
    return filtred

# Opção C: Busca com query parameters
@app.get("/buscar")
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 5):
    

    resultados = dados_cardapio 
    if nome:
        resultados = [x for x in resultados if nome.lower() in x["nome"].lower()]
    if categoria:
        resultados = [x for x in resultados if categoria.lower() in x["categoria"].lower()]
    
    resultados = resultados[:limite]
    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},
        "resultados": resultados,
        "total": len(resultados)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

id,nome,preco,categoria
1,Prato 1,10.50,Pizza
2,Prato 2,11.00,Lanches
3,Prato 3,11.50,Saladas
4,Prato 4,12.00,Pizza
5,Prato 5,12.50,Lanches
6,Prato 6,13.00,Saladas
7,Prato 7,13.50,Pizza
8,Prato 8,14.00,Lanches
9,Prato 9,14.50,Saladas
10,Prato 10,15.00,Pizza
11,Prato 11,15.50,Lanches
12,Prato 12,16.00,Saladas
13,Prato 13,16.50,Pizza
14,Prato 14,17.00,Lanches
15,Prato 15,17.50,Saladas
16,Prato 16,18.00,Pizza
17,Prato 17,18.50,Lanches
18,Prato 18,19.00,Saladas
19,Prato 19,19.50,Pizza
20,Prato 20,20.00,Lanches
21,Prato 21,20.50,Saladas
22,Prato 22,21.00,Pizza
23,Prato 23,21.50,Lanches
24,Prato 24,22.00,Saladas
25,Prato 25,22.50,Pizza
26,Prato 26,23.00,Lanches
27,Prato 27,23.50,Saladas
28,Prato 28,24.00,Pizza
29,Prato 29,24.50,Lanches
30,Prato 30,25.00,Saladas
31,Prato 31,25.50,Pizza
32,Prato 32,26.00,Lanches
33,Prato 33,26.50,Saladas
34,Prato 34,27.00,Pizza
35,Prato 35,27.50,Lanches
36,Prato 36,28.00,Saladas
37,Prato 37,28.50,Pizza
38,Prato 38,29.00,Lanches
39,Prato 39,29.50,Saladas
40,Prato 40,30.00,Pizza
41,Prato 41,30.50,Lanches
42,Prato 42,31.00,Saladas
43,Prato 43,31.50,Pizza
44,Prato 44,32.00,Lanches
45,Prato 45,32.50,Saladas
46,Prato 46,33.00,Pizza
47,Prato 47,33.50,Lanches
48,Prato 48,34.00,Saladas
49,Prato 49,34.50,Pizza
50,Prato 50,35.00,Lanches

# TESTE 4 --  combos, adição de novos pratos e execução da aplicação

from fastapi import Query
from typing import Tuple

# Gera todos combos possíveis com pratos de categorias diferentes
def gerar_todos_combos(cardapio: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any], float]]:
    itens = sorted(cardapio, key=lambda x: (x["preco"], x["id"]))
    combos = []
    n = len(itens)
    for a in range(n):
        for b in range(a + 1, n):
            if itens[a]["categoria"] != itens[b]["categoria"]:
                total = itens[a]["preco"] + itens[b]["preco"]
                combos.append((itens[a], itens[b], total))
    combos.sort(key=lambda t: (t[2], t[0]["id"], t[1]["id"]))
    return combos

TODOS_COMBOS = gerar_todos_combos(dados_cardapio)

# Endpoint que retorna combos diversos sem repetir pratos
@app.get("/cardapio/combos-diversidade", tags=["Combos"])
def combos_diversidade(qtd: int = Query(10, ge=1, le=50, description="Quantidade de combos a retornar")):
    if not TODOS_COMBOS:
        raise HTTPException(status_code=500, detail="Não foi possível gerar combos a partir do cardápio.")
    usados = set()
    selecionados = []
    for a, b, total in TODOS_COMBOS:
        if a["id"] in usados or b["id"] in usados:
            continue
        selecionados.append({
            "pratos": [a["id"], b["id"]],
            "categorias": [a["categoria"], b["categoria"]],
            "total": round(total, 2)
        })
        usados.add(a["id"])
        usados.add(b["id"])
        if len(selecionados) >= qtd:
            break
    if not selecionados:
        raise HTTPException(status_code=404, detail="Não foi possível montar combos diversos com os itens atuais.")
    return {
        "criterio": "diversidade (categorias diferentes) e sem repetir prato entre combos",
        "qtd": len(selecionados),
        "combos": selecionados
    }

# Endpoint para adicionar novo prato
@app.post("/dados", response_model=Prato, status_code=201, tags=["Dados"])
def adicionar_prato(novo_prato: Prato):
    if any(prato["id"] == novo_prato.id for prato in dados_cardapio):
        raise HTTPException(status_code=400, detail=f"ID {novo_prato.id} já existe.")
    dados_cardapio.append(novo_prato.dict())
    return novo_prato

# Executa o servidor local se o arquivo for rodado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



# TESTE 5 
from fastapi import Query
from typing import Tuple

# Gera todos combos possíveis com pratos de categorias diferentes
def gerar_todos_combos(cardapio: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any], float]]:
    itens = sorted(cardapio, key=lambda x: (x["preco"], x["id"]))
    combos = []
    n = len(itens)
    for a in range(n):
        for b in range(a + 1, n):
            if itens[a]["categoria"] != itens[b]["categoria"]:
                total = itens[a]["preco"] + itens[b]["preco"]
                combos.append((itens[a], itens[b], total))
    combos.sort(key=lambda t: (t[2], t[0]["id"], t[1]["id"]))
    return combos

TODOS_COMBOS = gerar_todos_combos(dados_cardapio)

# Endpoint que retorna combos diversos sem repetir pratos
@app.get("/cardapio/combos-diversidade", tags=["Combos"])
def combos_diversidade(qtd: int = Query(10, ge=1, le=50, description="Quantidade de combos a retornar")):
    if not TODOS_COMBOS:
        raise HTTPException(status_code=500, detail="Não foi possível gerar combos a partir do cardápio.")
    usados = set()
    selecionados = []
    for a, b, total in TODOS_COMBOS:
        if a["id"] in usados or b["id"] in usados:
            continue
        selecionados.append({
            "pratos": [a["id"], b["id"]],
            "categorias": [a["categoria"], b["categoria"]],
            "total": round(total, 2)
        })
        usados.add(a["id"])
        usados.add(b["id"])
        if len(selecionados) >= qtd:
            break
    if not selecionados:
        raise HTTPException(status_code=404, detail="Não foi possível montar combos diversos com os itens atuais.")
    return {
        "criterio": "diversidade (categorias diferentes) e sem repetir prato entre combos",
        "qtd": len(selecionados),
        "combos": selecionados
    }

# Endpoint para adicionar novo prato
@app.post("/dados", response_model=Prato, status_code=201, tags=["Dados"])
def adicionar_prato(novo_prato: Prato):
    if any(prato["id"] == novo_prato.id for prato in dados_cardapio):
        raise HTTPException(status_code=400, detail=f"ID {novo_prato.id} já existe.")
    dados_cardapio.append(novo_prato.dict())
    return novo_prato

# Executa o servidor local se o arquivo for rodado diretamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)





















# TESTE 5
# Importa as classes e funções necessárias
from fastapi import FastAPI, HTTPException, Query # Framework web e classe de exceção HTTP
from pydantic import BaseModel  # Para modelar e validar dados
import pandas as pd  # Biblioteca para manipulação de dados em DataFrames
import uvicorn  # Servidor ASGI para rodar a aplicação FastAPI
from typing import List, Dict, Any, Tuple
from pathlib import Path
import csv

# Cria a instância da aplicação FastAPI com título e versão
app = FastAPI(title="Minha API de Cardápio", version="1.0")

# Define um modelo de dados para validar e documentar pratos do cardápio
class Prato(BaseModel):
    id: int          # ID único do prato
    nome: str        # Nome do prato
    preco: float     # Preço do prato
    categoria: str   # Categoria do prato (Pizza, Lanches, Saladas...)

# Tenta carregar os dados do CSV na inicialização da aplicação
try:
    # Lê o CSV que está na pasta dados com o nome dataset_cardapio.csv
    df = pd.read_csv("dados/dataset_cardapio.csv")
    # Converte o DataFrame para uma lista de dicionários para uso no código Python
    dados_cardapio = df.to_dict(orient="records")
except Exception as e:
    # Caso ocorra erro (por exemplo, arquivo inexistente), imprime a mensagem e define lista vazia
    print(f"Erro ao carregar CSV: {e}")
    dados_cardapio = []

@app.get("/")
def home():
    """
    Endpoint raiz para dar informações básicas sobre a API.
    """
    return {
        "projeto": "Minha Primeira API",       # Nome do projeto
        "autor": "Raquel Santos Faria",                       # Autor 
        "descricao": "API para servir dados do cardápio",  # Breve descrição
        "total_registros": len(dados_cardapio)    # Quantidade total de pratos no cardápio
    }

@app.get("/dados", response_model=list[Prato])
def listar_todos():
    """
    Endpoint que retorna a lista completa de pratos.
    Usa o modelo Prato para resultados para validação e documentação.
    """
    return dados_cardapio                             # Retorna os dados carregados do CSV

@app.get("/dados/{item_id}", response_model=Prato)
def buscar_por_id(item_id: int):
    """
    Busca um prato específico pelo ID fornecido na URL.
    Se não encontrar o prato, lança uma exceção HTTP 404 com mensagem.
    """
    # Percorre os dados para encontrar o prato com ID igual ao informado
    for item in dados_cardapio:
        if item["id"] == item_id:
            return item                              # Retorna o prato encontrado
    # Se não encontrado, gera uma exceção HTTP com código 404 e detalhe do erro
    raise HTTPException(status_code=404, detail=f"Item com ID {item_id} não encontrado")

@app.get("/categoria/{categoria}", response_model=list[Prato])
def buscar_por_categoria(categoria: str):
    """
    Lista pratos filtrando pela categoria (ex: pizza, lanches), independente de serem maiúsculas ou minúsculas.
    """
   # Retorna os itens do cardápio cuja categoria coincide com a buscada, sem diferenciar letras maiúsculas de minúsculas
    return [item for item in dados_cardapio if item["categoria"].lower() == categoria.lower()]

@app.get("/buscar")
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 5):
    """
    Busca com filtros opcionais via Query Parameters:
    - nome: parte do nome do prato
    - categoria: categoria do prato
    - limite: limite máximo de resultados retornados
    """
    resultados = dados_cardapio                    # Começa com todos os dados
    # Filtra por nome se parâmetro nome estiver preenchido
    if nome:
        resultados = [item for item in resultados if nome.lower() in item["nome"].lower()]
    # Filtra por categoria se parâmetro categoria estiver preenchido
    if categoria:
        resultados = [item for item in resultados if item["categoria"].lower() == categoria.lower()]
    # Retorna os resultados limitados ao parâmetro limite solicitado
    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},   # Mostra filtros aplicados
        "resultados": resultados[:limite],                                    # Resultados paginados
        "total": len(resultados),                                             # Conte quantidade total de resultados
    }

# Ponto de entrada: sobe a API com Uvicorn somente se main.py for executado diretamente.
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)   # reload=True recarrega código automaticamente


# TESTE 6 - ENDPOINT CRIATIVO ADICIONAL -- alguns endpoints apareceram sem parâmetro no http://127.0.0.1:8000/docs
# Importa as classes e funções necessárias
from fastapi import FastAPI, HTTPException, Query  # Framework web e classe de exceção HTTP
from pydantic import BaseModel  # Para modelar e validar dados
import pandas as pd  # Biblioteca para manipulação de dados em DataFrames
import uvicorn  # Servidor ASGI para rodar a aplicação FastAPI
from typing import List, Dict, Any, Tuple  # Tipagens para ajudar o código
from pathlib import Path  # Para manipular caminhos do sistema operacional
import csv  # Para ler arquivos CSV manualmente

# Cria a instância da aplicação FastAPI com título e versão
app = FastAPI(title="Minha API de Cardápio", version="1.0")

# Define um modelo de dados para validar e documentar pratos do cardápio
class Prato(BaseModel):
    id: int          # ID único do prato
    nome: str        # Nome do prato
    preco: float     # Preço do prato
    categoria: str   # Categoria do prato (Pizza, Lanches, Saladas...)

# Função para carregar dados do CSV na inicialização da aplicação
def carregar_cardapio() -> List[Dict[str, Any]]:
    caminho = Path(__file__).parent / "dados" / "dataset_cardapio.csv"  # Define o caminho completo para o CSV
    if not caminho.exists():  # Se o arquivo não existir, lança exceção
        raise FileNotFoundError(f"CSV não encontrado em {caminho}")
    itens: List[Dict[str, Any]] = []
    # Abre o arquivo CSV para leitura com encoding adequado
    with caminho.open("r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            # Converte cada linha para o formato esperado e adiciona na lista
            itens.append({
                "id": int(row["id"]),
                "nome": row["nome"],
                "preco": float(row["preco"]),
                "categoria": row["categoria"]
            })
    return itens

# Carrega dados do CSV para a variável global ao iniciar
try:
    dados_cardapio = carregar_cardapio()
except FileNotFoundError as e:
    print(e)
    dados_cardapio = []  # Se falhar, mantém lista vazia para evitar crash da aplicação

# Endpoint raiz que retorna informações básicas da API
@app.get("/")
def home():
    return {
        "projeto": "Minha Primeira API",                 # Nome do projeto
        "autor": "Raquel Santos Faria",                   # Nome do autor
        "descricao": "API para servir dados do cardápio",  # Descrição breve
        "total_registros": len(dados_cardapio)           # Quantidade de pratos carregados
    }

# Endpoint que retorna todos os pratos do cardápio
@app.get("/dados", response_model=List[Prato])
def listar_todos():
    return dados_cardapio

# Endpoint que busca um prato pelo ID
@app.get("/dados/{item_id}", response_model=Prato)
def buscar_por_id(item_id: int):
    # Busca iterativamente o prato pelo ID
    for item in dados_cardapio:
        if item["id"] == item_id:
            return item
    # Se não encontrado, retorna erro 404
    raise HTTPException(status_code=404, detail=f"Item com ID {item_id} não encontrado")

# Endpoint que retorna pratos filtrados por categoria (case insensitive)
@app.get("/categoria/{categoria}", response_model=List[Prato])
def buscar_por_categoria(categoria: str):
    return [item for item in dados_cardapio if item["categoria"].lower() == categoria.lower()]

# Endpoint com busca flexível usando query parameters: nome, categoria e limite
@app.get("/buscar")
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 5):
    resultados = dados_cardapio
    if nome:
        resultados = [item for item in resultados if nome.lower() in item["nome"].lower()]
    if categoria:
        resultados = [item for item in resultados if item["categoria"].lower() == categoria.lower()]
    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},
        "resultados": resultados[:limite],
        "total": len(resultados),
    }

# Função para gerar todos combos possíveis de pratos de categorias diferentes
def gerar_todos_combos(cardapio: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any], float]]:
    itens = sorted(cardapio, key=lambda x: (x["preco"], x["id"]))  # Ordena por preco e id
    combos: List[Tuple[Dict[str, Any], Dict[str, Any], float]] = []
    n = len(itens)
    # Percorre todos os pares (a,b) para formar combos
    for a in range(n):
        for b in range(a + 1, n):
            if itens[a]["categoria"] != itens[b]["categoria"]:  # Apenas combos com categorias diferentes
                total = itens[a]["preco"] + itens[b]["preco"]
                combos.append((itens[a], itens[b], total))
    # Ordena combos por preço total, depois ids para estabilizar ordem
    combos.sort(key=lambda t: (t[2], t[0]["id"], t[1]["id"]))
    return combos

# Inicializa lista com todos os combos possíveis entre categorias diferentes
TODOS_COMBOS = gerar_todos_combos(dados_cardapio)

# Endpoint que retorna combos de pratos, garantindo diversidade e sem repetir pratos
@app.get("/cardapio/combos-diversidade")
def combos_diversidade(qtd: int = Query(10, ge=1, le=50, description="Quantidade de combos a retornar")):
    if not TODOS_COMBOS:
        raise HTTPException(status_code=500, detail="Não foi possível gerar combos a partir do cardápio.")
    usados: set[int] = set()  # Para evitar repetir pratos entre combos
    selecionados: List[Dict[str, Any]] = []
    # Itera sobre combos para selecionar os primeiros sem repetir pratos
    for a, b, total in TODOS_COMBOS:
        if a["id"] in usados or b["id"] in usados:
            continue
        selecionados.append({
            "pratos": [a["id"], b["id"]],
            "categorias": [a["categoria"], b["categoria"]],
            "total": round(total, 2)
        })
        usados.add(a["id"])
        usados.add(b["id"])
        if len(selecionados) >= qtd:
            break
    if not selecionados:
        raise HTTPException(status_code=404, detail="Não foi possível montar combos diversos com os itens atuais.")
    return {
        "criterio": "diversidade (categorias diferentes) e sem repetir prato entre combos",
        "qtd": len(selecionados),
        "combos": selecionados
    }

# Novo endpoint POST para adicionar um prato ao cardápio em memória
@app.post("/dados", response_model=Prato, status_code=201)
def adicionar_prato(novo_prato: Prato):
    # Verifica se o ID já existe para evitar duplicatas
    if any(prato["id"] == novo_prato.id for prato in dados_cardapio):
        raise HTTPException(status_code=400, detail=f"ID {novo_prato.id} já existe.")
    # Adiciona o novo prato no cardápio em memória
    dados_cardapio.append(novo_prato.dict())
    # NOTA: Persistir no CSV não está implementado nesta versão
    return novo_prato

# Executa o servidor localmente se este arquivo for executado diretamente
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# TESTE 8 -- corrige caminhos 

# Importa as classes do FastAPI para criar a aplicação e gerenciar exceções HTTP, além de permitir definir query params
from fastapi import FastAPI, HTTPException, Query  
# Importa BaseModel do Pydantic para validar e documentar dados de entrada e saída
from pydantic import BaseModel  
# Biblioteca para manipulação de dados tabulares (DataFrames)
import pandas as pd  
# Uvicorn é o servidor para rodar a aplicação FastAPI
import uvicorn  
# Importa tipos genéricos para tipagem das funções e variáveis do código
from typing import List, Dict, Any, Tuple  
# Para manipular caminhos de arquivo de modo portável, independente do sistema operacional
from pathlib import Path  
# Biblioteca para leitura e escrita de arquivos CSV
import csv  


# Cria a instância da aplicação FastAPI
app = FastAPI(title="Minha API de Cardápio", version="1.0")


# Define o modelo de dados 'Prato' para validar a estrutura dos dados do cardápio
class Prato(BaseModel):
    id: int          # Identificador único do prato
    nome: str        # Nome do prato
    preco: float     # Preço do prato
    categoria: str   # Categoria do prato, exemplo: 'Pizza', 'Lanches', 'Saladas'


# Função que carrega os dados do cardápio a partir de um arquivo CSV
def carregar_cardapio() -> List[Dict[str, Any]]:
    # Cria o caminho para o arquivo CSV 'dataset_cardapio.csv' dentro da pasta 'dados' no mesmo diretório do script
    caminho = Path(__file__).parent / "dados" / "dataset_cardapio.csv"
    
    # Verifica se o arquivo existe, caso contrário lança uma exceção de arquivo não encontrado
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado em {caminho}")
    
    # Inicializa uma lista vazia onde serão armazenados os pratos lidos do CSV
    itens: List[Dict[str, Any]] = []
    
    # Abre o arquivo para leitura, utilizando encoding adequado para evitar problemas com caracteres
    with caminho.open("r", encoding="utf-8-sig", newline="") as f:
        # Usa DictReader para ler cada linha como um dicionário
        r = csv.DictReader(f)
        # Itera sobre cada linha no CSV e converte os dados para tipos apropriados, adicionando-os na lista
        for row in r:
            itens.append({
                "id": int(row["id"]),              # Converte para inteiro
                "nome": row["nome"],              # Mantém como string
                "preco": float(row["preco"]),    # Converte para float
                "categoria": row["categoria"]    # Mantém como string
            })
    # Retorna a lista de pratos carregados do CSV
    return itens


# Tenta carregar o cardápio ao iniciar a aplicação
try:
    dados_cardapio = carregar_cardapio()
except FileNotFoundError as e:
    # Caso o arquivo CSV não seja encontrado, imprime o erro e inicializa o cardápio vazio
    print(e)
    dados_cardapio = []


# Endpoint raiz que retorna informações gerais sobre a API
@app.get("/", tags=["Informações"])
def home():
    # Retorna um dicionário com informações sobre o projeto, autor, descrição e total de pratos carregados
    return {
        "projeto": "Minha Primeira API",
        "autor": "Raquel Santos Faria",
        "descricao": "API para servir dados do cardápio",
        "total_registros": len(dados_cardapio)
    }


# Endpoint que retorna toda a lista de pratos
@app.get("/dados", response_model=List[Prato], tags=["Dados"])
def listar_todos():
    # Retorna a lista completa de pratos, garantindo que ela esteja conforme o modelo Prato
    return dados_cardapio


# Endpoint para buscar um prato pelo ID
@app.get("/dados/id/{item_id}", response_model=Prato, tags=["Dados"])
def buscar_por_id(item_id: int):
    # Itera sobre os pratos para encontrar o que corresponde ao ID fornecido
    for item in dados_cardapio:
        if item["id"] == item_id:
            return item  # Retorna o prato encontrado
    # Caso não encontre, lança exceção HTTP 404 com mensagem apropriada
    raise HTTPException(status_code=404, detail=f"Item com ID {item_id} não encontrado")


# Endpoint que retorna pratos filtrados por categoria, ignorando letras maiúsculas/minúsculas
@app.get("/dados/categoria/{categoria}", response_model=List[Prato], tags=["Dados"])
def buscar_por_categoria(categoria: str):
    # Retorna lista somente com pratos cuja categoria bate com a requisitada, caso-insensitive
    return [item for item in dados_cardapio if item["categoria"].lower() == categoria.lower()]


# Endpoint com múltiplos filtros opcionais por query parameters
@app.get("/dados/buscar", tags=["Dados"])
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 5):
    resultados = dados_cardapio
    # Filtra por nome parcial (se informado)
    if nome:
        resultados = [item for item in resultados if nome.lower() in item["nome"].lower()]
    # Filtra por categoria (se informado)
    if categoria:
        resultados = [item for item in resultados if item["categoria"].lower() == categoria.lower()]
    # Retorna os resultados limitados conforme o parâmetro limite
    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},  # Indica filtros aplicados
        "resultados": resultados[:limite],  # Resultados limitados
        "total": len(resultados),            # Total resultados encontrados
    }


# Função para gerar todos os combos possíveis com pratos de categorias diferentes
def gerar_todos_combos(cardapio: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any], float]]:
    # Ordena os pratos por preço e id para garantir ordenação determinística
    itens = sorted(cardapio, key=lambda x: (x["preco"], x["id"]))
    combos: List[Tuple[Dict[str, Any], Dict[str, Any], float]] = []
    n = len(itens)
    
    # Percorre todos os pares possíveis de pratos (sem repetição)
    for a in range(n):
        for b in range(a + 1, n):
            # Garante que os pratos tenham categorias diferentes para diversidade
            if itens[a]["categoria"] != itens[b]["categoria"]:
                # Calcula preço total do combo
                total = itens[a]["preco"] + itens[b]["preco"]
                # Adiciona o par e o total na lista de combos
                combos.append((itens[a], itens[b], total))
    
    # Ordena os combos pelo preço total crescente, depois pelo ID dos pratos para estabilidade
    combos.sort(key=lambda t: (t[2], t[0]["id"], t[1]["id"]))
    
    # Retorna a lista completa de combos
    return combos


# Carrega todos combos possíveis para uso rápido
TODOS_COMBOS = gerar_todos_combos(dados_cardapio)


# Endpoint que retorna combos diversos sem repetir pratos entre eles
@app.get("/cardapio/combos-diversidade", tags=["Combos"])
def combos_diversidade(qtd: int = Query(10, ge=1, le=50, description="Quantidade de combos a retornar")):
    # Caso não tenha combos gerados, retorna erro 500
    if not TODOS_COMBOS:
        raise HTTPException(status_code=500, detail="Não foi possível gerar combos a partir do cardápio.")
    
    usados: set[int] = set()  # Guarda IDs dos pratos já usados para evitar repetição
    selecionados: List[Dict[str, Any]] = []
    
    # Percorre todos os combos ordenados por preço e ID para selecionar os primeiros sem repetição
    for a, b, total in TODOS_COMBOS:
        if a["id"] in usados or b["id"] in usados:
            continue  # Ignora combos que tenham pratos já usados
        # Adiciona os combos selecionados com seus pratos, categorias e preço total arredondado
        selecionados.append({
            "pratos": [a["id"], b["id"]],
            "categorias": [a["categoria"], b["categoria"]],
            "total": round(total, 2)
        })
        # Marca os pratos como usados
        usados.add(a["id"])
        usados.add(b["id"])
        # Para se já tiver a quantidade solicitada
        if len(selecionados) >= qtd:
            break
    
    # Se não conseguiu formar combos, retorna erro 404
    if not selecionados:
        raise HTTPException(status_code=404, detail="Não foi possível montar combos diversos com os itens atuais.")
    
    # Retorna o critério usado, quantidade e a lista de combos
    return {
        "criterio": "diversidade (categorias diferentes) e sem repetir prato entre combos",
        "qtd": len(selecionados),
        "combos": selecionados
    }


# Endpoint POST para adicionar um novo prato ao cardápio
@app.post("/dados", response_model=Prato, status_code=201, tags=["Dados"])
def adicionar_prato(novo_prato: Prato):
    # Verifica se o ID informado já existe para evitar duplicação
    if any(prato["id"] == novo_prato.id for prato in dados_cardapio):
        raise HTTPException(status_code=400, detail=f"ID {novo_prato.id} já existe.")
    
    # Adiciona o novo prato na lista em memória
    dados_cardapio.append(novo_prato.dict())
    
    # Nota: persistência no CSV não está implementada
    return novo_prato


# Quando rodar esse arquivo diretamente, inicia o servidor Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
