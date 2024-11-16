from pybricks.hubs import PrimeHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color, Stop, Direction
from pybricks.tools      import wait, StopWatch

from bluetooth import comando_bt, TX_BRACO, TX_CABECA

import cores

def setup():
    global hub, motor_garra, sensor_cor_frente, ultra_dir, ultra_esq
    global garra_fechada, garra_resetada

    hub = PrimeHub(broadcast_channel=TX_BRACO, observe_channels=[TX_CABECA])
    print(hub.system.name())
    while hub.system.name() != "spike0":
        hub.speaker.beep(frequency=1024)
        wait(200)
    else:
        hub.light.blink(Color.ORANGE, [100,50,200,100])

    motor_garra       = Motor(Port.C)
    sensor_cor_frente = ColorSensor(Port.A)

    garra_fechada  = False
    garra_resetada = False

    hub.system.set_stop_button((Button.CENTER,))
    return hub

def fecha_garra(motor_garra, vel=240):
    global garra_fechada, garra_resetada
    print("fecha_garra:")
    motor_garra.run_until_stalled(vel)
    motor_garra.run_angle(vel, 30, then=Stop.COAST, wait=False)
    garra_fechada = True
    garra_resetada = False

def abre_garra(motor_garra, vel=240, ang_volta=42):
    global garra_fechada, garra_resetada
    print("abre_garra:")
    motor_garra.run_angle(vel, -ang_volta, then=Stop.COAST, wait=True)

    garra_fechada = False
    garra_resetada = False

def reseta_garra(motor_garra):
    global garra_fechada, garra_resetada
    fecha_garra(motor_garra)
    abre_garra(motor_garra, ang_volta=60)

    garra_resetada = True
    garra_fechada = False

def main():
    while True:
        comando = hub.ble.observe(TX_CABECA)
        if comando is not None:
            print(comando)
            comando, *args = comando
        else: continue

        if   comando == comando_bt.fecha_garra:
            print("main: pediu fecho")
            if not garra_fechada:
                fecha_garra(motor_garra)
            hub.ble.broadcast((comando_bt.fechei,))
        elif comando == comando_bt.abre_garra:
            print("main: pediu abre")
            if garra_fechada:
                abre_garra(motor_garra)
            hub.ble.broadcast((comando_bt.abri,))
        elif comando == comando_bt.reseta_garra:
            print("main: pediu reset")
            if not garra_resetada:
                reseta_garra(motor_garra)
            hub.ble.broadcast((comando_bt.resetei,))

        elif comando == comando_bt.ver_cor_passageiro:
            print("main: pediu cor")
            cor = sensor_cor_frente.color() #! reclassificar co hsv se der NONE
            hub.ble.broadcast((comando_bt.cor_passageiro, cores.Color2cor(cor)))
        elif comando == comando_bt.ver_hsv_passageiro:
            print("main: pediu cor")
            cor = sensor_cor_frente.hsv()
            hub.ble.broadcast((comando_bt.hsv_passageiro, cores.Color2tuple(cor)))
        elif comando == comando_bt.ver_distancias:
            print("main: pediu dist")
            dist_esq, dist_dir = ultra_esq.distance(), ultra_dir.distance()
            hub.ble.broadcast((comando_bt.distancias, dist_esq, dist_dir))
