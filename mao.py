from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Button, Color, Direction

from pybricks.tools      import wait, StopWatch

import garra

def setup(hub):
    global motor_garra, motor_gira

    motor_garra = Motor(Port.F, Direction.COUNTERCLOCKWISE)
    motor_gira  = Motor(Port.E)

    hub.system.set_stop_button((Button.CENTER,))


def main(hub):
    garra.fecha_garra(motor_garra, motor_gira)
    wait(300)
    garra.abre_garra(motor_garra, motor_gira)
