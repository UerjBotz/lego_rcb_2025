from lib.polyfill import Enum

from lib.bipes import bipe_inicio, bipe_final

ID = Enum("ID", ["BRACO", "CABECA", "TESTE"])
id = ID.CABECA

if id == ID.CABECA:
    import cabeca
    hub = cabeca.setup()
    
    bipe_inicio(hub)
    cabeca.main(hub)
    bipe_final(hub)
elif id == ID.BRACO:
    import braco
    hub = braco.setup()

    bipe_inicio(hub)
    braco.main(hub)
    bipe_final(hub)

elif id == ID.TESTE:
    from pybricks.hubs import PrimeHub

    from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor

    from pybricks.parameters import Port, Axis, Stop, Direction, Button, Color
    from pybricks.tools      import wait, StopWatch
    from pybricks.robotics   import DriveBase
    
    hub = PrimeHub()
    
    bipe_inicio(hub)
    ...
    bipe_final(hub)
else:
    assert False

