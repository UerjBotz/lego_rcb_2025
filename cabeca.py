from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color

from pybricks.tools      import wait, StopWatch
from pybricks.robotics   import DriveBase

import cores

def setup(hub):
    global rodas, botao_calibrar, sensor_cor

    sensor_cor = ColorSensor(Port.D)
    roda_esq   = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    roda_dir   = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

    rodas = DriveBase(roda_esq, roda_dir,
                      wheel_diameter=88, axle_track=145.5) #! ver depois se recalibrar

    botao_calibrar = Button.CENTER

    hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))


def tela_escolher_cor(hub, selecao):
    tam_max = max(map(len, iter(cores.cor)))
    on_max, off_max = 150, 30
    
    cor = cores.cor(selecao)
    tam_cor = len(cor)
    tam_rel = tam_cor/tam_max

    letra_on  =    int(on_max /tam_rel)
    letra_off = 10+int(off_max/tam_rel/2)

    hub.display.text(cor, on=letra_on, off=letra_off) #! mudar pra gerador e fazer letra a letra
    wait(100)

def menu_calibracao(hub, sensor_cor, botao_parar=Button.UP,
                                     botao_aceitar=Button.CENTER,
                                     botao_anterior=Button.LEFT,
                                     botao_proximo=Button.RIGHT):
    selecao = 0

    while True:
        tela_escolher_cor(hub, selecao)
        botões = hub.buttons.pressed()

        if   botao_proximo  in botões:
            selecao = (selecao + 1) % len(cores.cor)
        elif botao_anterior in botões:
            selecao = (selecao - 1) % len(cores.cor)

        elif botao_aceitar in botões:
            hub.display.text("CALIBRANDO...")
            cores.mapa_rgb[selecao], *cores.mapa_hsv[selecao] = (
                cores.calibrar(hub, sensor_cor, botao_aceitar)
            )
        elif botao_parar   in botões: break

def main(hub):
    while True:
        botões = hub.buttons.pressed()
        if botao_calibrar in botões:
            hub.speaker.beep(frequency=300, duration=100)

            menu_calibracao(hub, sensor_cor) 
            print(cores.mapa_rgb)
            print(cores.mapa_hsv)

            break
