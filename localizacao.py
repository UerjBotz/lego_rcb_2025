from dataclasses import dataclass
from typing import Dict, Union, List

@dataclass
class Celula:
    """Classe para guardar dados de cada celula domapa"""
    tipo: str #rua ou edificio
    
@dataclass
class Edificio(Celula):
    entradas: list = None # lista de entradas
    canos_colocados: Dict[str, bool] = None #dictque marca quais entradas ja tem canos

@dataclass
class Rua(Celula):
    ocupada: bool = False

CelulaTipo = Union[Edificio, Rua]

def cria_matriz():
    """Cria uma matriz 5x5 com celulas do tipo Rua e Edificio"""
    return matriz

def definir_edificios(matriz: List[List[CelulaTipo]], x, y, entradas: List[str]):
    """Define os edificios na matriz"""
    pass

def imprime_matriz(matriz):
    """Imprime a matriz"""
    pass


if __name__ == "__main__":
    matriz = cria_matriz()
    definir_edificios(matriz)
    imprime_matriz(matriz)