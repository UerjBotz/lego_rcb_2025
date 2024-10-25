#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)

from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools      import wait, StopWatch, DataLog
from pybricks.robotics   import DriveBase

from pybricks.media.ev3dev import Font#, SoundFile, ImageFile

from math import ceil
import cores

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Create your objects here.
ev3 = EV3Brick()

sensor_cor     = ColorSensor(Port.S4)
botao_calibrar = Button.CENTER
botao_anterior = Button.LEFT
botao_proximo  = Button.RIGHT
botao_começar  = Button.UP

tam_fonte = 15
ev3.screen.set_font(Font('Lucida', size=tam_fonte, monospace=True))

# Write your program here.
ev3.speaker.beep(frequency=500, duration=100)

#TODO: passar +1/-1 em vez do número da seleção, ou fazer a lógica de botão aqui direto
def tela_calibração(hub, seleção, force_clear=False, pad=5,
                                  text_height=tam_fonte+4,
                                  text_width=ev3.screen.width//2):
    if force_clear: hub.screen.clear()

    cor_normal      = (Color.BLACK, Color.WHITE)
    cor_selecionado = (Color.WHITE, Color.BLACK)

    start_x = start_y = pad
    for i, texto in enumerate(cores.cor):
        selecionado = (i == seleção)

        front, back = cor_selecionado if selecionado else cor_normal

        qtd_lin     = len(cores.cor)
        qtd_lin_col = ceil(qtd_lin/2)

        x = start_x + text_width *(i >= qtd_lin_col)
        y = start_y + text_height*(i %  qtd_lin_col)

        hub.screen.draw_text(x,y, texto, text_color=front,
                                         background_color=back)

frame, seleção = 0, 0
while True:
    tela_calibração(ev3, seleção, force_clear=False)#=(frame % 10 == 0))

    botões = ev3.buttons.pressed()
    if   botao_calibrar in botões:
        cor = cores.calibrar(ev3, sensor_cor, botao_calibrar)
        print(cor)

        break
    elif botao_proximo  in botões:
        seleção = (seleção + 1) % len(cores.cor)
        wait(100)
    elif botao_anterior in botões:
        seleção = (seleção - 1) % len(cores.cor)
        wait(100)
    
    elif botao_começar  in botões:
        break #! fazer coisas aqui
    
    frame += 1

ev3.speaker.beep(frequency=250, duration=200)
