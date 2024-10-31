MAX_DIST = 2000

def coleta_dists (hub, ultra, botao_parar):
    dists = []
    while botao_parar not in hub.buttons.pressed():
        dist = ultra.distance()
        if dist < MAX_DIST:
            print(dist)
            #dists.append(dist)

    return dists

