from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union, List
from pybricks.parameters import Color


tipoCelula = Enum("tipoCelula",
                  [
                    "RUA", 
                    "EDIFICIO"
                   ])

tiposEntradas = Enum("tiposEntradas",
                     ["N", "S", "L", "O"])

nomesEdificios = Enum("nomesEdificios",
                      [
                          "PARK", "BAKERY", "SCHOOL", "DRUGSTORE", 
                          "CITY HALL", "MUSEUM", "LIBRARY",
                      ])

coresEdificios = Enum("coresEdificios",
                      [
                          Color.GREEN, Color.BROWN, Color.BLUE, Color.RED,
                          Color.GREEN, Color.BLUE, Color.BROWN                           
                      ])

@dataclass
class Celula:
    """Classe para guardar dados de cada celula domapa"""
    tipo: tipoCelula #rua ou edificio
    
@dataclass
class Edificio(Celula):
    nome: nomesEdificios
    cor: Color
    entradas: list[tiposEntradas] = None # lista de entradas
    canos_colocados: Dict[tiposEntradas, bool] = None #dictque marca quais entradas ja tem canos

    def __post_init__(self):
        self.tipo = tipoCelula.EDIFICIO
        if self.canos_colocados == None:
            self.canos_colocados = {entrada: False for entrada in (self.entradas or [])}

@dataclass
class Rua(Celula):
    ocupada: bool = False
    
    def __post_init__(self):
        self.tipo = tipoCelula.RUA

def cria_matriz() -> List[List[Celula]]:
    """Cria uma matr iz 6x5(verificar tamanho) com celulas do tipo Rua e Edificio"""
    return [[Rua(tipo=tipoCelula.RUA) for _ in range(5)] for _ in range(6)]

def preenche_matriz(matriz):
    pass

def definir_edificios(matriz: List[List[Celula]], x, y, entradas: List[str]):
    """Define os edificios na matriz"""
    matriz[x][y] = Edificio(tipo=tipoCelula.EDIFICIO, entradas=entradas)

def imprime_matriz(matriz):
    """Imprime a matriz"""
    pass

def coloca_obstaculo(matriz, Celula, x, y):
    pass

def tira_obstaculo(matriz, Celula, x, y):
    pass

if __name__ == "__main__":
    pass