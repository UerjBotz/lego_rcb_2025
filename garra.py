from pybricks.parameters import Port, Stop
from pybricks.tools      import wait

def fecha_garra(motor_garra, motor_gira, vel=240):
    motor_garra.run_until_stalled(vel, then=Stop.COAST, duty_limit=None) #! async

    motor_gira.run_target(vel, 90, then=Stop.HOLD, wait=True) #! async

def abre_garra(motor_garra, motor_gira, vel=240):
    motor_gira.run_target(vel,  0, then=Stop.HOLD, wait=True) #! async

    motor_garra.run_angle(vel,-100, then=Stop.COAST, wait=True) #! async

#motor_roda.run_time(speed, time, then=Stop.HOLD, wait=True)
