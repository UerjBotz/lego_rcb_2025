from polyfill import Enum

import bipes

ID = Enum("ID", ["BRACO", "CABECA", "TESTE"])
id = ID.CABECA

if id == ID.CABECA:
    import cabeca
    hub = cabeca.setup()
    
    bipes.inicio(hub)
    cabeca.main(hub)
    bipes.final(hub)
elif id == ID.BRACO:
    import braco
    hub = braco.setup()

    bipes.inicio(hub)
    braco.main(hub)
    bipes.final(hub)

elif id == ID.TESTE:
    from pybricks.hubs import PrimeHub

    from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor

    from pybricks.parameters import Port, Axis, Stop, Direction, Button, Color
    from pybricks.tools      import wait, StopWatch
    from pybricks.robotics   import DriveBase
    
    hub = PrimeHub()
    
    bipes.inicio(hub)
    ...
    bipes.final(hub)
else:
    assert False

