from pybricks.hubs import PrimeHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color, Direction
from pybricks.tools      import wait, StopWatch

from bluetooth import comando_bt, TX_BRACO, TX_CABECA

import cores
import garra

def assert_hub(hub, nome_esperado):
    print(hub.system.name())
    while hub.system.name() != nome_esperado:
        hub.speaker.beep(frequency=1024)
        wait(200)

def setup():
    global hub, motor_garra, motor_vertical, sensor_cor_frente, ultra_dir, ultra_esq
    global garra_fechada, garra_levantada

    hub = PrimeHub(broadcast_channel=TX_BRACO, observe_channels=[TX_CABECA])
    assert_hub(hub, "spike0")
    hub.light.blink(Color.ORANGE, [100,50,200,100])

    motor_garra       = Motor(Port.B, Direction.COUNTERCLOCKWISE)
    motor_vertical    = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    sensor_cor_frente = ColorSensor(Port.D)

    garra_fechada = False
    garra_levantada = False

    hub.system.set_stop_button((Button.CENTER,))
    return hub

def main(hub):
    global garra_fechada, garra_levantada

    while True:
        comando = hub.ble.observe(TX_CABECA)
        if comando is not None:
            print(comando)
            comando, *args = comando
        else: continue

        if   comando == comando_bt.fecha_garra:
            print("pediu fecho")
            if not garra_fechada:
                print("fechando")
                garra.fecha_garra(motor_garra)
                garra_fechada = True
            hub.ble.broadcast((comando_bt.fechei,))
        elif comando == comando_bt.abre_garra:
            print("pediu abre")
            if garra_fechada:
                print("abrindo")
                garra.abre_garra(motor_garra)
                garra_fechada = False
            hub.ble.broadcast((comando_bt.abri,))

        elif comando == comando_bt.levanta_garra:
            print("pediu levanto")
            if not garra_levantada:
                print("levantando")
                garra.levanta_garra(motor_vertical)
                garra_levantada = True
            hub.ble.broadcast((comando_bt.levantei,))
        elif comando == comando_bt.abaixa_garra:
            print("pediu abaixo")
            if garra_levantada:
                print("abaixando")
                garra.abaixa_garra(motor_vertical)
                garra_levantada = False
            hub.ble.broadcast((comando_bt.abaixei,))
            
        elif comando == comando_bt.ver_cor_passageiro:
            print("pediu cor")
            cor = sensor_cor_frente.color() #! reclassificar co hsv se der NONE
            hub.ble.broadcast((comando_bt.cor_passageiro, cores.Color2cor(cor)))
        elif comando == comando_bt.ver_hsv_passageiro:
            print("pediu cor")
            cor = sensor_cor_frente.hsv()
            hub.ble.broadcast((comando_bt.hsv_passageiro, cores.Color2tuple(cor)))

