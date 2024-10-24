#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick

from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)

from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools      import wait, StopWatch, DataLog
from pybricks.robotics   import DriveBase

from pybricks.media.ev3dev import Font#, SoundFile, ImageFile

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

ev3.screen.set_font(Font('Lucida', size=11, monospace=True))

# Write your program here.
ev3.speaker.beep(frequency=500, duration=100)

def tela(seleção, clear=True, redraw=True,
                  pad=10, text_height=11,
                  text_width=ev3.screen.width//2):
    if clear:
        ev3.screen.clear()

    start_x = start_y = pad
    for i, texto in enumerate(cores.cor):
        x = start_x if i < len(cores.cor) else start_x + text_width
        y = (start_y + text_height*i) % ev3.screen.height

        selecionado = i == seleção

        front, back = ((Color.WHITE, Color.BLACK) if selecionado else 
                       (Color.BLACK, Color.WHITE))
        ev3.screen.draw_text(x,y, texto, text_color=front,
                                         background_color=back)

frame = 0
seleção = 0
while True:
    if frame % 10 == 0:
        tela(seleção, clear=True)
    else:
        tela(seleção, clear=False)

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
