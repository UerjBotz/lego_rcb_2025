from dataclasses import dataclass
# from polyfill import Enum
from enum import Enum
from typing import Dict, Union, List
from pybricks.parameters import Color
from cores import cor


tipo_celula = Enum("tipo_celula",
                  [
                    "RUA", 
                    "EDIFICIO"
                   ])

tipo_parede = Enum("tipo_parede",
                    ["PAREDE", "ENTRADA", "ENTRADA_COM_CANO"]
                    )

class posicao_parede(Enum):
    N = 0
    S = 1
    L = 2
    O = 3

@dataclass
class Edificio():
    nome: str
    cor: int #enum cor
    tipo = tipo_celula.EDIFICIO
    paredes: list[tipo_parede] = None # lista de entradas
    ocupada: bool = True

@dataclass
class Rua():
    ocupada: bool = False
    tipo = tipo_celula.RUA
    
celula = Edificio | Rua
# "N", "S", "L", "O" 
bakery = Edificio(
    nome = "BAKERY",
    cor = cor.MARROM,
    paredes = [tipo_parede.PAREDE, tipo_parede.ENTRADA, tipo_parede.PAREDE, tipo_parede.ENTRADA]
)
school = Edificio(
    nome = "SCHOOL",
    cor = cor.AZUL,
    paredes = [tipo_parede.PAREDE, tipo_parede.ENTRADA, tipo_parede.PAREDE, tipo_parede.ENTRADA]
)
drugstore = Edificio(
    nome = "DRUGSTORE",
    cor = cor.VERMELHO,
    paredes = [tipo_parede.PAREDE, tipo_parede.PAREDE, tipo_parede.ENTRADA, tipo_parede.ENTRADA]
)
city_hall = Edificio(
    nome = "CITY HALL",
    cor = cor.VERDE,
    paredes = [tipo_parede.ENTRADA, tipo_parede.ENTRADA, tipo_parede.PAREDE, tipo_parede.PAREDE]
)
museum = Edificio(
    nome = "MUSEUM",
    cor = cor.AZUL,
    paredes = [tipo_parede.ENTRADA, tipo_parede.PAREDE, tipo_parede.ENTRADA, tipo_parede.PAREDE]
)
library = Edificio(
    nome = "LIBRARY",
    cor = cor.VERMELHO,
    paredes = [tipo_parede.ENTRADA, tipo_parede.PAREDE, tipo_parede.ENTRADA, tipo_parede.PAREDE]
)
park_aberto = Edificio(
    nome = "PARK",
    cor = cor.VERDE,
    paredes = [tipo_parede.PAREDE, tipo_parede.PAREDE, tipo_parede.ENTRADA, tipo_parede.PAREDE]
)
park_fechado = Edificio(
    nome = "PARK",
    cor = cor.VERDE,
    paredes = [tipo_parede.PAREDE, tipo_parede.PAREDE, tipo_parede.PAREDE, tipo_parede.PAREDE]
)

  
def imprime_matriz(matriz):
    """Imprime a matriz de forma alinhada."""
    largura_maxima = 12
    
    for linha in matriz:
        for celula in linha:
            if celula.tipo == tipo_celula.EDIFICIO:
                texto = celula.nome
            else:
                texto = "OBSTACULO" if celula.ocupada else "RUA"
            print(texto.ljust(largura_maxima), end=" ")
        print()

def coloca_obstaculo(x, y):
    if mapa[x][y].tipo == tipo_celula.EDIFICIO:
        return
    mapa[x][y].ocupada = True

def tira_obstaculo(x, y):
    if mapa[x][y].tipo == tipo_celula.EDIFICIO:
        return
    mapa[x][y].ocupada = False

def coloca_passageiro(edificio: Edificio, entrada: str): #ver como faz para escolher a entrada para ocupar
    if edificio.tipo == tipo_celula.RUA:
        return False
    entradas_ocupadas = map(lambda parede: parede != tipo_parede.ENTRADA, edificio.paredes)
    if all(entradas_ocupadas):
        return False
    if entrada != "N" and entrada != "S" and entrada != "L" and entrada != "O":
        return False
    edificio.paredes[posicao_parede[entrada]] = tipo_parede.ENTRADA_COM_CANO
    return True
    
mapa = [
    [park_aberto,   Rua(),  bakery,     Rua(),  school,     Rua()],
    [park_fechado,  Rua(),  Rua(),      Rua(),  Rua(),      Rua()],
    [park_aberto,   Rua(),  drugstore,  Rua(),  city_hall,  Rua()],
    [park_fechado,  Rua(),  Rua(),      Rua(),  Rua(),      Rua()],
    [park_aberto,   Rua(),  museum,     Rua(),  library,    Rua()],
]


from queue import PriorityQueue
import math

#direcoes (i,j)
direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Movimentos: direita, baixo, esquerda, cima

def heuristica(posicao_atual, destino):
    """Função heurística usando a distância de Manhattan."""
    return abs(posicao_atual[0] - destino[0]) + abs(posicao_atual[1] - destino[1])

def dentro_dos_limites(matriz, x, y):
    """Verifica se uma posição está dentro dos limites da matriz."""
    return 0 <= x < len(matriz) and 0 <= y < len(matriz[0])

def a_estrela(mapa, inicio, destino):
    """Implementação do algoritmo A* para encontrar o caminho mais curto."""
    fila_prioridade = PriorityQueue()
    fila_prioridade.put((0, inicio))
    g_custo = {inicio: 0}
    caminho = {}
    
    while not fila_prioridade.empty():
        _, atual = fila_prioridade.get()

        if atual == destino:
            # Reconstrução do caminho
            caminho_reverso = []
            while atual in caminho:
                caminho_reverso.append(atual)
                atual = caminho[atual]
            caminho_reverso.append(inicio)
            return caminho_reverso[::-1]  # Retorna o caminho na ordem correta

        x, y = atual
        for dx, dy in direcoes:
            vizinho = (x + dx, y + dy)
            if dentro_dos_limites(mapa, vizinho[0], vizinho[1]) and not mapa[vizinho[0]][vizinho[1]].ocupada:
                g = g_custo[atual] + 1  # Assume custo uniforme para mover de uma célula para outra
                if vizinho not in g_custo or g < g_custo[vizinho]:
                    g_custo[vizinho] = g
                    f = g + heuristica(vizinho, destino)
                    fila_prioridade.put((f, vizinho))
                    caminho[vizinho] = atual

    return None  # Retorna None se nenhum caminho for encontrado

if __name__ == "__main__":
    posicao_inicial = (0, 1)
    posicao_final = (4, 4)
    print("Mapa Original:")
    imprime_matriz(mapa)
    # coloca_obstaculo(2, 3)
    print("\nMapa com obstáculo:")
    imprime_matriz(mapa)
    
    resutado = a_estrela(mapa, posicao_inicial, posicao_final)
    print(resutado)
    