from lib.bipes import bipe_inicio, bipe_final, bipe_falha

CABECA = "spike0"
BRACO = "spike1"

id = hub

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

    while True:
        try:
            bipe_inicio(hub)
            braco.main(hub)
            bipe_final(hub)
        except Exception as e:
            bipe_falha(hub)
            print(f"{e}")
            continue
else:
    assert False

