from pybricks.parameters import Port, Stop
from pybricks.tools      import wait

DIST_GARRA = 600

def fecha_garra(motor_garra, vel=240):
    motor_garra.run_until_stalled(vel, then=Stop.COAST, duty_limit=None)
    motor_garra.run_angle(vel, 30, then=Stop.COAST, wait=False)

def abre_garra(motor_garra, vel=240, ang_volta=42):
    motor_garra.run_angle(vel, -ang_volta, then=Stop.COAST, wait=True)

def levanta_garra(motor_vertical, vel=240):
    motor_vertical.run_angle(vel, DIST_GARRA, then=Stop.COAST, wait=True)

def abaixa_garra(motor_vertical, vel=240):
    motor_vertical.run_until_stalled(vel, then=Stop.COAST, duty_limit=None)
    #motor_vertical.run_angle(-vel, DIST_GARRA, then=Stop.COAST, wait=True)
