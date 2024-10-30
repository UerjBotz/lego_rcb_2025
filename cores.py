from pybricks.tools      import wait
from pybricks.parameters import Button

from umath import sqrt
from polyfill import Enum, rgb_to_hsv, hsv_to_rgb


def calibrar(hub, sensor, botao_parar, ev3=None, spike=None) -> tuple[rgb, rgb, rgb]:
    wait(200)

    minm, maxm = (1, 1, 1), (0, 0, 0)
    soma, cont = (0, 0, 0), 0
    while botao_parar not in hub.buttons.pressed():
        if   ev3:
            rgb = sensor.rgb()
            hsv = rgb_to_hsv(rgb)
        elif spike:
            hsv = sensor.hsv()
            rgb = hsv_to_rgb(hsv)
        else:
            raise Exception("hub inválido")
        rgb_norm = tuple(map(lambda pct: pct/100, rgb))

        minm = tuple(map(min, minm, hsv))
        maxm = tuple(map(max, maxm, hsv))

        soma = tuple(map(lambda c,s: c+s, rgb_norm, soma))
        cont += 1

        cor_txt = tuple(map("{:.2f}".format, rgb_norm))
        print(cor_txt, "max:", maxm, "min:", minm)

    med = tuple(map(lambda s: s/cont, soma))
    return (med, minm, maxm)

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


def identificar_cor_hsv(hsv) -> cor:
    h, s, v = hsv
    for i, (m, M) in mapa_hsv:
        hm, _, _ = m
        hM, _, _ = M

        if h in range(m, M): return i

def dist(cor1, cor2) -> float:
    #! tem que ver se faz sentido usar com hsv também, mas a conta funciona
    r1, g1, b1 = cor1
    r2, g2, b2 = cor2
    return sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

def identificar_cor_dist(rgb) -> cor:
    #! teria como usar com hsv também, mas usa o outro mapa
    min_dist, min_idx = 1, -1
    for i, cor_canonica in enumerate(mapa_rgb):
        d = dist(rgb, cor_canonica)
        if d < min_dist:
            min_dist = d
            min_idx  = i

    return min_idx

def identificar(rgb=None, hsv=None) -> cor:
    if   rgb is not None:
        hsv = rgb_to_hsv(rgb)
    elif hsv is not None:
        rgb = hsv_to_rgb(hsv)
    else:
        raise ValueError("esperada cor de entrada")

    return identificar_cor_dist(rgb) #ou identificar_cor_hsv(hsv)

