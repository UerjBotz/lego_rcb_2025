from lib.polyfill    import Enum, heappop, heappush
from cores           import cor

tipo_celula = Enum("tipo_celula", ["RUA", "CRUZ", "BORDA", "ENTRADA"])

tipo_parede = Enum("tipo_parede", ["PAREDE",
                                   "ENTRADA",
                                   "ENTRADA_COM_CANO"])

posicao_parede = Enum("posicao_parede", ["N", "L", "S", "O"])

"""
map = [
    [BORDA, BORDA,]
]
    
"""

class Rua:
    def __init__(self, cruz=True):
        self.tipo = tipo_celula.RUA
        self.cruz = cruz

class Borda:
    def __init__(self, entrada=True):
        self.tipo = tipo_celula.BORDA
        self.entrada = entrada

# celula = Edificio | Rua

def imprime_matriz(matriz):
    """Imprime a matriz de forma alinhada."""
    largura_maxima = 12

    for linha in matriz:
        for celula in linha:
            if celula.tipo == tipo_celula.RUA:
                texto = 'ENTRADA' if celula.borda else 'RUA'
            else:
                texto = 'CRUZAMENTO' if self.borda
            print(texto.ljust(largura_maxima), end=" ")
        print()

def coloca_obstaculo(x, y):
    if mapa[x][y].tipo == tipo_celula.EDIFICIO: return #! falhar mais alto

    mapa[x][y].ocupada = True

def tira_obstaculo(x, y):
    if mapa[x][y].tipo == tipo_celula.EDIFICIO: return

    mapa[x][y].ocupada = False

def coloca_passageiro(edificio: Edificio, entrada: str): #ver como faz para escolher a entrada para ocupar
    if edificio.tipo == tipo_celula.RUA: return False
    if entrada not in "NSLO":            return False

    idx = posicao_parede[entrada]
    if edificio.paredes[idx] != tipo_parede.ENTRADA: return False

    if all(map(lambda p: p != tipo_parede.ENTRADA, edificio.paredes)):
        return False #! falhar mais alto

    edificio.paredes[idx] = tipo_parede.ENTRADA_COM_CANO
    return True

bakery = Edificio(
    nome = "BAKERY",
    cor = cor.MARROM,
    paredes = {
        posicao_parede.N: tipo_parede.PAREDE,
        posicao_parede.S: tipo_parede.ENTRADA,
        posicao_parede.L: tipo_parede.PAREDE,
        posicao_parede.O: tipo_parede.ENTRADA
    }
)
school = Edificio(
    nome = "SCHOOL",
    cor = cor.AZUL,
    paredes = {
        posicao_parede.N: tipo_parede.PAREDE,
        posicao_parede.S: tipo_parede.ENTRADA,
        posicao_parede.L: tipo_parede.PAREDE,
        posicao_parede.O: tipo_parede.ENTRADA
    }
)
drugstore = Edificio(
    nome = "DRUGSTORE",
    cor = cor.VERMELHO,
    paredes = {
        posicao_parede.N: tipo_parede.PAREDE,
        posicao_parede.S: tipo_parede.PAREDE,
        posicao_parede.L: tipo_parede.ENTRADA,
        posicao_parede.O: tipo_parede.ENTRADA
    }
)
city_hall = Edificio(
    nome = "CITY HALL",
    cor = cor.VERDE,
    paredes = {
        posicao_parede.N: tipo_parede.ENTRADA,
        posicao_parede.S: tipo_parede.ENTRADA,
        posicao_parede.L: tipo_parede.PAREDE,
        posicao_parede.O: tipo_parede.PAREDE
    }
)
museum = Edificio(
    nome = "MUSEUM",
    cor = cor.AZUL,
    paredes = {
        posicao_parede.N: tipo_parede.ENTRADA,
        posicao_parede.S: tipo_parede.PAREDE,
        posicao_parede.L: tipo_parede.ENTRADA,
        posicao_parede.O: tipo_parede.PAREDE
    }
)
library = Edificio(
    nome = "LIBRARY",
    cor = cor.VERMELHO,
    paredes = {
        posicao_parede.N: tipo_parede.ENTRADA,
        posicao_parede.S: tipo_parede.PAREDE,
        posicao_parede.L: tipo_parede.ENTRADA,
        posicao_parede.O: tipo_parede.PAREDE
    }
)
park_aberto = lambda: Edificio(
    nome = "PARK",
    cor = cor.VERDE,
    paredes = {
        posicao_parede.N: tipo_parede.PAREDE,
        posicao_parede.S: tipo_parede.PAREDE,
        posicao_parede.L: tipo_parede.ENTRADA,
        posicao_parede.O: tipo_parede.PAREDE
    }
)
park_fechado = lambda: Edificio(
    nome = "PARK",
    cor = cor.VERDE,
    paredes = {
        posicao_parede.N: tipo_parede.PAREDE,
        posicao_parede.S: tipo_parede.PAREDE,
        posicao_parede.L: tipo_parede.PAREDE,
        posicao_parede.O: tipo_parede.PAREDE
    }
)
#! ver se lambdar os outros também

mapa = [
    [park_aberto(),   Rua(),  bakery,     Rua(),  school,     Rua()],
    [park_fechado(),  Rua(),  Rua(),      Rua(),  Rua(),      Rua()],
    [park_aberto(),   Rua(),  drugstore,  Rua(),  city_hall,  Rua()],
    [park_fechado(),  Rua(),  Rua(),      Rua(),  Rua(),      Rua()],
    [park_aberto(),   Rua(),  museum,     Rua(),  library,    Rua()],
]

## implementação do A* (adaptada de <https://www.geeksforgeeks.org/a-search-algorithm-in-python/>)
class Cell():
    def __init__(self, i_pai=0,
                       j_pai=0,
                       f=float('inf'),
                       g=float('inf'),
                       h=0):
        self.i_pai = i_pai # Parent cell's row index
        self.j_pai = j_pai # Parent cell's column index
        self.f     = f # Total cost of the cell (g + h)
        self.g     = g # Cost from start to this cell
        self.h     = h # Heuristic cost from this cell to destination

direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Movimentos: direita, baixo, esquerda, cima

def dist_manhatan(posicao_atual, destino):
    atual_x, atual_y = posicao_atual
    dest_x,  dest_y  = destino
    return abs(atual_x - dest_x) + abs(atual_y - dest_y)

def dentro_dos_limites(matriz, cell):
    x, y = cell
    return 0 <= x < len(matriz) and 0 <= y < len(matriz[0])

def celula_livre(grid, cell):
    row, col = cell
    return not grid[row][col].ocupada

def eh_destino(src, dest): #! acho que dá pra mudar isso pra parar em frente à porta
    row, col = src
    return row == dest[0] and col == dest[1]

def heuristica(src, dest):
    return dist_manhatan(src, dest)

# Trace the path from source to destination
def tracar_caminho(info_celulas, dest):
    print("The Path is ")
    path = []
    row, col = dest

    # Trace the path from destination to source using parent cells
    while not (info_celulas[row][col].i_pai == row and info_celulas[row][col].j_pai == col):
        path.append((row, col))
        temp_row = info_celulas[row][col].i_pai
        temp_col = info_celulas[row][col].j_pai
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()
    
    return path

# Implement the A* search algorithm
def a_estrela(grid, src, dest):
    ok = True
    if not dentro_dos_limites(grid, src):
        ok = False; print(f"a_estrela: origem inválida {src}")
    if not dentro_dos_limites(grid, dest):
        ok = False; print(f"a_estrela: destino inválido {dest}")

    if not celula_livre(grid, src):
        ok = False; print(f"a_estrela: origem bloqueada {src}")
    if not celula_livre(grid, dest):
        ok = False; print(f"a_estrela: destino bloqueado {dest}")

    if not ok: return None

    # Check if we are already at the destination
    if eh_destino(src, dest):
        print(f"a_estrela: já no destino {src, dest}"); return []

    ROW = len(grid)
    COL = len(grid[0])

    # Initialize the closed list (visited cells)
    closed_list  = [[False for _ in range(COL)]  for _ in range(ROW)]
    # Initialize the details of each cell
    info_celulas = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i, j = src
    info_celulas[i][j] = Cell(f=0,
                              g=0,
                              h=0,
                              i_pai=i,
                              j_pai=j)

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    achou_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        for dir in direcoes:
            new_i = i + dir[0]
            new_j = j + dir[1]
            new = new_i, new_j

            # If the successor is valid, unblocked, and not visited
            if dentro_dos_limites(grid, new) and celula_livre(grid, new) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if eh_destino(new, dest):
                    # Set the parent of the destination cell
                    info_celulas[new_i][new_j].i_pai = i
                    info_celulas[new_i][new_j].j_pai = j
                    print("a_estrela: caminho encontrado")
                    # Trace and print the path from source to destination
                    return tracar_caminho(info_celulas, dest)
                else:
                    # Calculate the new f, g, and h values
                    g_new = info_celulas[i][j].g + 1.0
                    h_new = heuristica(new, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if info_celulas[new_i][new_j].f == float('inf') or info_celulas[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        info_celulas[new_i][new_j] = Cell(f = f_new,
                                                          g = g_new,
                                                          h = h_new,
                                                          i_pai = i,
                                                          j_pai = j)

    # If the destination is not found after visiting all cells
    if not achou_dest:
        print("a_estrela: não achou")

    return None

#funcao que recebe lista de posicoes na matriz e transforma em lista de direcoes
def caminho_relativo(caminho_absoluto: list[tuple[int, int]]):
    if caminho_absoluto is None:
        caminho_absoluto = []
        print("Caminho Errado")

    #movimentos
    direita = (0, 1); baixo = (1, 0); esquerda = (0, -1); cima = (-1, 0)
    direcoes = [(0,0)]

    # print(caminho_absoluto)
    for i in range(1, len(caminho_absoluto)):
        dx = caminho_absoluto[i][0] - caminho_absoluto[i - 1][0]
        dy = caminho_absoluto[i][1] - caminho_absoluto[i - 1][1]

        if   dx == 0 and dy == 1:
            direcoes.append(direita)
        elif dx == 1 and dy == 0:
            direcoes.append(baixo)
        elif dx == 0 and dy == -1:
            direcoes.append(esquerda)
        elif dx == -1 and dy == 0:
            direcoes.append(cima)

    return direcoes #! checar no chamador se é vazio

tipo_movimento = Enum("tipo_movimento",
                      ["FRENTE", "DIREITA_FRENTE", "ESQUERDA_FRENTE", "TRAS", "DIREITA", "ESQUERDA"])

def prox_movimento(ori_ini: tipo_movimento, ori_final: tipo_movimento): #type: ignore
        diferenca = (ori_final - ori_ini) % 4
        if   diferenca == 0: return tipo_movimento.FRENTE
        elif diferenca == 1: return tipo_movimento.DIREITA_FRENTE
        elif diferenca == 2: return tipo_movimento.TRAS
        elif diferenca == 3: return tipo_movimento.ESQUERDA_FRENTE
        else:
            assert False

def movimento_relativo(cam_rel, orientacao_ini):
    idx_orientacao = posicao_parede[orientacao_ini]
    nova_orientacao = orientacao_ini

    caminho_relativo = cam_rel.copy()
    caminho_relativo.pop(0)

    movimentos = []
    for movimento in caminho_relativo:
        if   movimento == ( 0, 1): nova_orientacao = "L"
        elif movimento == ( 1, 0): nova_orientacao = "S"
        elif movimento == ( 0,-1): nova_orientacao = "O"
        elif movimento == (-1, 0): nova_orientacao = "N"

        nova_idx_orientacao = posicao_parede[nova_orientacao]

        movimentos.append(
            prox_movimento(idx_orientacao, nova_idx_orientacao)
        )

        idx_orientacao = nova_idx_orientacao

    return movimentos


def achar_movimentos(pos_ini, pos_fim, orientacao):
    lin, col = pos_fim
    
    indice = next((i for i, valor in mapa[lin][col].paredes.items() if valor == tipo_parede.ENTRADA))
    print(f"achar_movimentos: {indice=}")
    
    if indice is None:
        print("achar_movimentos: não há entradas disponíveis")
        return []
    
    orientacao_final = None
    if   indice == posicao_parede.N:
        pos_fim = (lin-1, col)
        orientacao_final = "S"
        print(f"achar_movimentos: pos_parede=N: {indice=}, {orientacao_final=}")
    elif indice == posicao_parede.S:
        pos_fim = (lin+1, col)
        orientacao_final = "N"
        print(f"achar_movimentos: pos_parede=S: {indice=}, {orientacao_final=}")
    elif indice == posicao_parede.L:
        pos_fim = (lin, col+1)
        orientacao_final = "O"
        print(f"achar_movimentos: pos_parede=O: {indice=}, {orientacao_final=}")
    elif indice == posicao_parede.O:
        pos_fim = (lin, col-1)
        orientacao_final = "L"
        print(f"achar_movimentos: pos_parede=L: {indice=}, {orientacao_final=}")
    else:
        print(f"achar_movimentos: {indice=}: {pos_ini=}, {pos_fim=}. {orientacao=}, {orientacao_final=}")
        assert False
    
    caminho     = a_estrela(mapa, pos_ini, pos_fim)
    print("achar_movimentos:", *caminho, sep=" -> ")
    caminho_rel = caminho_relativo(caminho)
    print(f"achar_movimentos: {caminho_rel=}")

    return (movimento_relativo(caminho_rel, orientacao), orientacao_final) #! tratar orientação final None e caminho vazio no chamador
