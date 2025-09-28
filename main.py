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
