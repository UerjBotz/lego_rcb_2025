from pybricks.tools      import wait
from pybricks.parameters import Button

from umath import sqrt
from polyfill import Enum, rgb_to_hsv, hsv_to_rgb

from _cores_calibradas import mapa_rgb, mapa_hsv

def calibrar(hub, sensor, botao_parar, ev3=None, spike=True) -> tuple[rgb, rgb, rgb]:
    wait(200)

    minm, maxm = (1, 1, 1), (0, 0, 0)
    soma, cont = (0, 0, 0), 0
    while botao_parar not in hub.buttons.pressed():
        if   ev3:
            rgb = sensor.rgb()
            hsv = rgb_to_hsv(rgb)
            rgb_norm = tuple(map(lambda pct: pct/100, rgb))
        elif spike:
            hsv = sensor.hsv()
            hsv = hsv.h, hsv.s, hsv.v
            
            rgb_norm = hsv_to_rgb((hsv[0]/360, hsv[1]/100, hsv[2]/100))
        else:
            raise Exception("hub inválido")

        minm = tuple(map(min, minm, hsv))
        maxm = tuple(map(max, maxm, hsv))

        soma = tuple(map(lambda c,s: c+s, rgb_norm, soma))
        cont += 1

        cor_txt_rgb = tuple(map("{:.2f}".format, rgb_norm))
        cor_txt_hsv = tuple(map("{:.2f}".format, hsv))
        print(cor_txt_hsv, cor_txt_rgb, "max:", maxm, "min:", minm)
        
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


def salvar_cores():
    global mapa_rgb, mapa_hsv
    
    print(f"mapa_rgb = [")
    for c in range(len(cor)):
        print(f"\t{mapa_rgb[c]}, #{cor(c)}")
    print("]")
    
    print(f"mapa_hsv = [")
    for c in range(len(cor)):
        print(f"\t{mapa_hsv[c]}, #{cor(c)}")
    print("]")
