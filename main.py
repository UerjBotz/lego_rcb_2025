from pybricks.hubs import EV3Brick

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)

from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools      import wait, StopWatch, DataLog
from pybricks.robotics   import DriveBase

from pybricks.media.ev3dev import Font#, SoundFile, ImageFile

from math import ceil
import cores

# This program was only tested using LEGO EV3 MicroPython v2.0

# Create your objects here.
ev3 = EV3Brick()

sensor_cor     = ColorSensor(Port.S4)
botao_calibrar = Button.CENTER

tam_fonte = 15
ev3.screen.set_font(Font('Lucida', size=tam_fonte, monospace=True))

# Write your program here.
def tela_escolher_cor(hub, selecao, pad=5,
                                    text_height=tam_fonte+4,
                                    text_width=ev3.screen.width//2):
    cor_normal      = (Color.BLACK, Color.WHITE)
    cor_selecionado = (Color.WHITE, Color.BLACK)

    start_x = start_y = pad
    for i, texto in enumerate(cores.cor):
        selecionado = (i == selecao)

        front, back = cor_selecionado if selecionado else cor_normal

        qtd_lin     = len(cores.cor)
        qtd_lin_col = ceil(qtd_lin/2)

        x = start_x + text_width *(i >= qtd_lin_col)
        y = start_y + text_height*(i %  qtd_lin_col)

        hub.screen.draw_text(x,y, texto, text_color=front,
                                         background_color=back)

def menu_calibracao(hub, sensor_cor, botao_parar=Button.UP,
                                     botao_aceitar=Button.CENTER,
                                     botao_anterior=Button.LEFT,
                                     botao_proximo=Button.RIGHT):
    selecao = 0

    hub.screen.clear()
    tela_escolher_cor(hub, selecao)

    wait(150)
    botões = hub.buttons.pressed()
    while True:
        if   botao_proximo  in botões:
            selecao = (selecao + 1) % len(cores.cor)
            tela_escolher_cor(hub, selecao)
        elif botao_anterior in botões:
            selecao = (selecao - 1) % len(cores.cor)
            tela_escolher_cor(hub, selecao)

        elif botao_aceitar in botões:
            hub.screen.clear()
            hub.screen.draw_text(hub.screen.width//6, hub.screen.height//3, 
                                 "CALIBRANDO...",
                                 text_color=Color.WHITE,
                                 background_color=Color.BLACK)
            cores.mapa_rgb[selecao], *cores.mapa_hsv[selecao] = (
                cores.calibrar(hub, sensor_cor, botao_aceitar)
            )
            hub.screen.clear()
            tela_escolher_cor(hub, selecao)
        elif botao_parar   in botões: break

        wait(150)
        botões = hub.buttons.pressed()

ev3.speaker.beep(frequency=500, duration=100)

while True:
    botões = ev3.buttons.pressed()
    if botao_calibrar in botões:
        ev3.speaker.beep(frequency=300, duration=100)

        menu_calibracao(ev3, sensor_cor) 
        print(cores.mapa_rgb)
        print(cores.mapa_hsv)

        break

ev3.speaker.beep(frequency=250, duration=200)
