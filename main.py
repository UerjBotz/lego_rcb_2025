from pybricks.hubs import PrimeHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor

from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools      import wait, StopWatch
from pybricks.robotics   import DriveBase

import cores
import garra

ID_CABECA = 1
ID_MAO    = 0

# Create your objects here.
hub = PrimeHub()
id_robo = ID_MAO

def setup_cabeca(hub):
    global rodas, botao_calibrar

    #sensor_cor = ColorSensor(Port.A)
    roda_esq   = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    roda_dir   = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

    rodas = DriveBase(roda_esq, roda_dir,
                      wheel_diameter=88, axle_track=145.5) #! ver depois se recalibrar

    botao_calibrar = Button.CENTER

    hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))

def setup_mao():
    global motor_garra, motor_gira

    motor_garra = Motor(Port.F)
    motor_gira  = Motor(Port.E)

    hub.system.set_stop_button((Button.CENTER,))

if   id_robo == ID_CABECA:
    setup_cabeca()
elif id_robo == ID_MAO:
    setup_mao()
else:
    pass # testar aqui

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

def main_cabeca():
    while True:
        botões = hub.buttons.pressed()
        if botao_calibrar in botões:
            hub.speaker.beep(frequency=300, duration=100)

            menu_calibracao(hub, sensor_cor) 
            print(cores.mapa_rgb)
            print(cores.mapa_hsv)

            break

def main_mao():
    garra.fecha_garra(motor_garra, motor_gira)
    wait(300)
    garra.abre_garra(motor_garra, motor_gira)

hub.speaker.beep(frequency=500, duration=100)

if   id_robo == ID_CABECA:
    main_cabeca()
elif id_robo == ID_MAO:
    main_mao()
else:
    pass # teste aqui

hub.speaker.beep(frequency=250, duration=200)
