from pybricks.hubs import PrimeHub

import cabeca
import mao

from polyfill import Enum

ID = Enum("ID", ["MAO", "CABECA", "TESTE"])

# "constantes"
id = ID.CABECA
hub = PrimeHub()

# main
hub.speaker.beep(frequency=500, duration=100)

if id == ID.CABECA:
    cabeca.setup(hub)
    cabeca.main(hub)
elif id == ID.MAO:
    mao.setup(hub)
    mao.main(hub)
elif id == ID.TESTE:
    ...
else:
    assert False

hub.speaker.beep(frequency=250, duration=200)
