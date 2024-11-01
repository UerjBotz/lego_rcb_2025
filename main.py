import cabeca
import braco

from polyfill import Enum

ID = Enum("ID", ["MAO", "CABECA", "TESTE"])
id = ID.CABECA

if id == ID.CABECA:
    hub = cabeca.setup()
    
    hub.speaker.beep(frequency=500, duration=100)
    cabeca.main(hub)
    hub.speaker.beep(frequency=250, duration=200)
elif id == ID.MAO:
    hub = braco.setup()

    hub.speaker.beep(frequency=500, duration=100)
    braco.main()
    hub.speaker.beep(frequency=250, duration=200)
elif id == ID.TESTE:
    ...
else:
    assert False

