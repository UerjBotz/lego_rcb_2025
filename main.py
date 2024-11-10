from lib.polyfill import Enum

from lib.bipes import bipe_inicio, bipe_final

ID = Enum("ID", ["BRACO", "CABECA", "TESTE"])
id = ID.TESTE

if id == ID.CABECA:
    import cabeca
    hub = cabeca.setup()
    print(hub.battery.voltage())

    bipe_inicio(hub)
    cabeca.main(hub)
    bipe_final(hub)
elif id == ID.BRACO:
    import braco
    hub = braco.setup()
    print(hub.battery.voltage())

    bipe_inicio(hub)
    braco.main(hub)
    bipe_final(hub)

elif id == ID.TESTE:
    from pybricks.hubs import PrimeHub

    from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor

    from pybricks.parameters import Port, Axis, Stop, Direction, Button, Color
    from pybricks.tools      import wait, StopWatch
    from pybricks.robotics   import DriveBase

    import cores
    import cabeca
    from lib.bipes import *

    hub = cabeca.setup()
    print(hub.battery.voltage())

    bipe_inicio(hub)
    while True:
        if Button.CENTER in hub.buttons.pressed():
            bipe_calibracao(hub)
            #! levar os dois sensores em consideração separadamente
            mapa_hsv = cabeca.menu_calibracao(hub, cabeca.sensor_cor_esq, cabeca.sensor_cor_dir)
            cores.repl_calibracao(mapa_hsv)#, lado="esq")
            while Button.CENTER not in hub.buttons.pressed():
                pass
        hsv_esq = cabeca.sensor_cor_esq.hsv()
        hsv_dir = cabeca.sensor_cor_dir.hsv()
        cor_esq  = cores.cor(cores.identificar(hsv_esq))
        cor_dir  = cores.cor(cores.identificar(hsv_dir))
        color_esq = cabeca.sensor_cor_esq.color()
        color_dir = cabeca.sensor_cor_dir.color()
        print(f"{cor_esq=}\t{cor_dir=}\t|\t{color_esq=}\t{color_dir=}")

    bipe_final(hub)
else:
    assert False

