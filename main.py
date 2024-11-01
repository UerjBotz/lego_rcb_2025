import cabeca
import mao

from polyfill import Enum

ID = Enum("ID", ["MAO", "CABECA", "TESTE"])
id = ID.TESTE

if id == ID.CABECA:
    hub = cabeca.setup()
    
    hub.speaker.beep(frequency=500, duration=100)
    cabeca.main(hub)
    hub.speaker.beep(frequency=250, duration=200)
elif id == ID.MAO:
    hub = mao.setup()

    hub.speaker.beep(frequency=500, duration=100)
    mao.main()
    hub.speaker.beep(frequency=250, duration=200)

elif id == ID.TESTE:
    from pybricks.hubs import PrimeHub
    from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor

    from pybricks.parameters import Port, Axis, Stop, Direction, Button, Color
    from pybricks.tools      import wait, StopWatch
    from pybricks.robotics   import DriveBase
    
    #hub = PrimeHub()
    hub = PrimeHub(top_side=Axis.X, front_side=-Axis.Z) #! sinais dos eixos
    #rodas.use_gyro(True) #! testar depois, funcionou pior/inconsistente

    roda_esq   = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    roda_dir   = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

    rodas = DriveBase(roda_esq, roda_dir,
                      wheel_diameter=88, axle_track=145.5) #! ver depois se recalibrar
    
    #battery_voltage = hub.battery.voltage()
    #print(battery_voltage)

    rodas.straight(300)
    rodas.turn(360, then=Stop.BRAKE, wait=True)
    #rodas.turn(360, then=Stop.BRAKE, wait=False)
    #while not rodas.done():
    #    print(hub.imu.heading())
    
    # while True:
    #    print(hub.imu.tilt())

else:
    assert False
