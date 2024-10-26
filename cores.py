from pybricks.tools      import wait
from pybricks.parameters import Button

from math import sqrt
from polyfill import Enum, rgb_to_hsv

def calibrar(hub, sensor, botao_parar) -> tuple[rgb, rgb, rgb]:
    wait(200)

    minm, maxm = (1, 1, 1), (0, 0, 0)
    soma, cont = (0, 0, 0), 0
    while botao_parar not in hub.buttons.pressed():
        cor = sensor.rgb()
        cor_norm = tuple(map(lambda pct: pct/100, cor))

        minm = tuple(map(min, minm, cor_norm))
        maxm = tuple(map(max, maxm, cor_norm))
        soma = tuple(map(lambda c,s: c+s, cor_norm, soma))
        cont += 1

        cor_txt = tuple(map("{:.2f}".format, cor_norm))
        print(cor_txt, "max:", maxm, "min:", minm)

    med = tuple(map(lambda s: s/cont, soma))
    return (minm, maxm, med)

cor = Enum("cor", ["AMARELO",
                   "VERDE",
                   "AZUL",
                   "VERMELHO",
                   "MARROM",
                   "CINZA", #! ver se dá pra usar de verdade
                   "PRETO",
                   "BRANCO"])
mapa_rgb = [ (0, 0, 0)             for _ in range(len(cor))]
mapa_hsv = [((0, 0, 0), (0, 0, 0)) for _ in range(len(cor))]


def identificar_cor_hsv(cor_entrada) -> cor:
    h, s, v = rgb_to_hsv(cor_entrada)
    for i, (m, M) in mapa_hsv:
        hm, _, _ = m
        hM, _, _ = M

        if h in range(m, M): return i

def dist(rgb1, rgb2) -> float:
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def identificar_cor_dist(cor_entrada) -> cor:
    min_dist, min_idx = 1, -1
    for i, cor_canonica in enumerate(mapa_cores):
        d = dist(cor_entrada, cor_canonica)
        if d < min_dist:
            min_dist = d
            min_idx  = i
    
    return min_idx

def identificar(cor_entrada) -> cor:
    return identificar_cor_dist(cor_entrada)

