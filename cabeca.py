from pybricks.hubs import PrimeHub

from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Side, Direction, Button, Color

from pybricks.tools      import wait, StopWatch
from pybricks.robotics   import DriveBase

from lib.bipes import bipe_calibracao, bipe_cabeca, musica_vitoria, musica_derrota

from urandom import choice

import cores
import gui
import bluetooth as blt


TAM_BLOCO   = 300
TAM_BLOCO_Y = 294 # na nossa arena os quadrados não são 30x30cm (são 29.4 por quase 30)

TAM_FAIXA = 30
TAM_BLOCO_BECO = TAM_BLOCO_Y - TAM_FAIXA # os blocos dos becos são menores por causa do vermelho

DIST_EIXO_SENSOR = 80 #mm
DIST_EIXO_SENS_DIST = 45 #mm   #! checar

DIST_PASSAGEIRO_RUA = 220 #! checar


def setup():
    global hub, sensor_cor_esq, sensor_cor_dir, rodas
    global botao_calibrar, rodas_conf_padrao
    
    hub = PrimeHub(broadcast_channel=blt.TX_CABECA, observe_channels=[blt.TX_BRACO])

    hub.display.orientation(Side.BOTTOM)
    hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))

    sensor_cor_esq = ColorSensor(Port.D)
    sensor_cor_dir = ColorSensor(Port.C)

    roda_esq = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    roda_dir = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

    rodas = DriveBase(roda_esq, roda_dir,
                      wheel_diameter=88, axle_track=145.5) #! ver depois se recalibrar

    botao_calibrar = Button.CENTER
    rodas_conf_padrao = rodas.settings()

    return hub

class mudar_velocidade():
    """
    gerenciador de contexto (bloco with) para (automaticamente):
    1. mudar a velocidade do robô
    2. restaurar a velocidade do robô
    """
    def __init__(self, rodas, vel): 
        self.rodas = rodas
        self.vel   = vel
 
    def __enter__(self): 
        self.conf_anterior = self.rodas.settings()
        _, *conf_resto     = self.conf_anterior
        self.rodas.settings(self.vel, *conf_resto)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.rodas.settings(*self.conf_anterior)

def dar_meia_volta():
    rodas.turn(180)
    rodas.straight(TAM_BLOCO)

DIST_PARAR=-0.4
def parar():
    rodas.straight(DIST_PARAR)
    rodas.stop()
ANG_PARAR=-0.0
def parar_girar():
    rodas.turn(ANG_PARAR)
    rodas.stop()

def dar_re(dist):
    rodas.straight(-dist)

def re_meio_bloco(eixo_menor=False):
    if eixo_menor:
        dar_re(TAM_BLOCO_Y//2 - DIST_EIXO_SENSOR)
    else:
        dar_re(TAM_BLOCO//2   - DIST_EIXO_SENSOR)

def ver_nao_pista():
    cor_esq = sensor_cor_esq.color()
    cor_dir = sensor_cor_dir.color()
    return ((not cores.pista(cor_esq) or not cores.pista(cor_dir)),
            cor_esq, cor_dir)

def ver_passageiro_perto():
    dist_esq, dist_dir = blt.ver_distancias(hub)
    return ((dist_esq < DIST_PASSAGEIRO_RUA or dist_dir < DIST_PASSAGEIRO_RUA),
            dist_esq, dist_dir)

def ver_obstaculo():
    recuo = TAM_BLOCO*3//2
    dist_esq, dist_dir = blt.ver_distancias(hub)
    return (dist_esq <= recuo or dist_dir <= recuo,
            dist_esq, dist_dir)

def evitar_obstaculo():
    rodas.turn(90)
    viu, *dists = ver_obstaculo()
    if not viu:
        print("SEM OBSTACULO")
        print(dists)
        rodas.turn(-90)
    else:
        print("TEM OBSTACULO")
        print(dists)

    foi_terminado, *dists = andar_ate(ver_obstaculo, dist_max=TAM_BLOCO*4)
    dist_perco = rodas.distance()
    print(f"Distância percorrida até ver:{dist_perco}")

def andar_ate(*conds_parada: Callable, dist_max=TAM_BLOCO*6) -> tuple[bool, Any]: # type: ignore
    rodas.reset()
    rodas.straight(dist_max, wait=False)
    while not rodas.done():
        for i, cond_parada in enumerate(conds_parada):
            chegou, *retorno = cond_parada()
            if not chegou: continue
            else:
                parar()
                return i+1, retorno
    return 0, (rodas.distance(),)

def achar_limite() -> tuple[Color, hsv, Color, hsv]: # type: ignore
    cor_esq, cor_dir = andar_ate(ver_nao_pista)

    hsv_esq = sensor_cor_esq.hsv()
    hsv_dir = sensor_cor_dir.hsv()
    return (cor_esq, hsv_esq, cor_dir, hsv_dir)

def achar_azul():
    cor_esq, hsv_esq, cor_dir, hsv_dir = achar_limite() # anda reto até achar o limite

    if   cores.beco(cor_esq) or cores.beco(cor_dir): #! beco é menor que os outros blocos
        print(f"achar_azul:91: {cor_esq=}, {cor_dir=}")

        re_meio_bloco()
        dar_re(TAM_BLOCO_BECO) 
        rodas.turn(choice((90, -90)))
        
        cor_esq, hsv_esq, cor_dir, hsv_dir = achar_limite() # anda reto até achar o limite
        print(f"achar_azul:97: {cor_esq=}, {cor_dir=}")

        if cores.parede_hsv(hsv_esq) or cores.parede_hsv(hsv_dir): rodas.turn(180)

        cor_esq, hsv_esq, cor_dir, hsv_dir = achar_limite() # anda reto até achar o limite
        print(f"achar_azul:105: {cor_esq=}, {cor_dir=}")

        return cores.certificar(sensor_cor_dir, sensor_cor_esq, Color.BLUE)
    elif cores.parede(cor_esq) or cores.parede(cor_dir): #! hsv
        print(f"achar_azul:109: {cor_esq=}, {cor_dir=}")

        re_meio_bloco()
        rodas.turn(90)

        return False
    else: #azul
        print(f"achar_azul:114: {cor_esq=}, {cor_dir=}")

        cor_esq, hsv_esq, cor_dir, hsv_dir = achar_limite() # anda reto até achar o limite
        print(f"achar_azul:117: {cor_esq=}, {cor_dir=}")

        if cores.certificar(sensor_cor_dir, sensor_cor_esq, Color.BLUE):
            return True
        else:
            re_meio_bloco()
            rodas.turn(90)
            return False

def alinhar():
    while True:
        cor_dir = sensor_cor_dir.color()
        cor_esq = sensor_cor_esq.color()

        print(cor_dir, cor_esq)

        ang_girado = 0.0
        dist_percorrida = 0.0
        rodas.straight(TAM_BLOCO/10, wait=False)
        if rodas.distance() > TAM_BLOCO*4//5:
            dar_re(rodas.distance())
            rodas.turn(90)
            rodas.reset()
            continue

        if not cores.pista(cor_esq) or not cores.pista(cor_dir):
            parar()
            dist_percorrida = rodas.distance()
            if not cores.pista(cor_esq) and not cores.pista(cor_dir):
                print("ENTREI RETO")
                dar_re(dist_percorrida)
                return True
            else:
                print("ENTREI TORTO")
                rodas.turn(-90, wait=False)
                cor_dir = sensor_cor_dir.color()
                cor_esq = sensor_cor_esq.color()
                if not (cores.pista(cor_dir) ^ cores.pista(cor_esq)):
                    print("cor_igual")
                    parar_girar()
                    ang_girado = rodas.angle()
                    rodas.turn(-ang_girado)
                    dar_re(dist_percorrida)
                    rodas.turn(ang_girado)

                    rodas.turn(90)
                    rodas.reset()
                    return alinhar()

def pegar_passageiro():
    print("pegar passageiro")
    with mudar_velocidade(rodas, 50):
        regra_corresp, info = andar_ate(ver_nao_pista, ver_passageiro_perto,
                                        dist_max=TAM_BLOCO*4)
    if   regra_corresp == 1:
        print("regra 1")
        #! checar se vermelho mesmo
        (cor_esq, cor_dir) = info
        print(f"{cor_esq=}, {cor_dir=}")
        re_meio_bloco()
        rodas.turn(180)
        return False # é pra ter chegado no vermelho
    elif regra_corresp == 2:
        print("regra 2")
        (dist_esq, dist_dir) = info
        dist = dist_esq if dist_esq < dist_dir else dist_dir
        ang  = -90      if dist_esq < dist_dir else 90
        #! inverti a virada aqui, checar se não tão invertidos na definição

        blt.abrir_garra(hub)
        dar_re(DIST_EIXO_SENS_DIST-20) #! desmagificar
        rodas.turn(ang)
        rodas.straight(dist)
        blt.fechar_garra(hub)
        cor_cano = blt.ver_cor_passageiro(hub)
        print(cores.cor(cores.identificar(cor_cano)))

        if cores.identificar(cor_cano) == cores.cor.BRANCO:
            blt.abrir_garra(hub)
            rodas.straight(-dist)
            rodas.turn(-ang)
            return False
        return True
    else:
        rodas.turn(180)
        return False #chegou na distância máxima

def pegar_primeiro_passageiro() -> bool:
    print("pegando passageiro")
    #! a cor é pra ser azul
    rodas.turn(90)
    achar_limite()
    #! a cor é pra ser vermelha
    rodas.turn(180)
    pegou = pegar_passageiro()
    while not pegou:
        pegou = pegar_passageiro()
    
    return True


def menu_calibracao(hub, sensor_esq, sensor_dir,
                                     botao_parar=Button.BLUETOOTH,
                                     botao_aceitar=Button.CENTER,
                                     botao_anterior=Button.LEFT,
                                     botao_proximo=Button.RIGHT):
    mapa_hsv = cores.mapa_hsv.copy()

    selecao = 0

    wait(150)
    while True:
        botões = gui.tela_escolher_cor(hub, cores.cor, selecao)

        if   botao_proximo  in botões:
            selecao = (selecao + 1) % len(cores.cor)
            wait(100)
        elif botao_anterior in botões:
            selecao = (selecao - 1) % len(cores.cor)
            wait(100)

        elif botao_aceitar in botões:
            [wait(100) for _ in gui.mostrar_palavra(hub, "CAL..")]
            mapa_hsv[selecao] = (
                cores.coletar_valores(hub, botao_aceitar, dir=sensor_dir, esq=sensor_esq)
            )
            wait(150)
        elif botao_parar   in botões:
            wait(100)
            return mapa_hsv


def main(hub):
    crono = StopWatch()
    while crono.time() < 100: #! ativar calibração quando for usar
        botões = hub.buttons.pressed()
        if botao_calibrar in botões:
            bipe_calibracao(hub)
            #! levar os dois sensores em consideração separadamente
            mapa_hsv = menu_calibracao(hub, sensor_cor_esq, sensor_cor_dir)
            cores.repl_calibracao(mapa_hsv)#, lado="esq")
            return

    hub.system.set_stop_button((Button.BLUETOOTH,))
    bipe_cabeca(hub)

    #! antes de qualquer coisa, era bom ver se na sua frente tem obstáculo
    #! sobre isso ^ ainda, tem que tomar cuidado pra não confundir eles com os passageiros

    evitar_obstaculo()
    return

    alinhou = achou_azul = False
    while not alinhou:
        alinhou = alinhar()
    while not achou_azul:
        achou_azul = achar_azul()
    #achar_limite()
    pegou = pegar_primeiro_passageiro()
    if pegou:
        dar_meia_volta()
        blt.abrir_garra(hub)
        musica_vitoria(hub)
    else:
        musica_derrota(hub)
        wait(1000)
        return #! fazer main retornar que nem em c e tocar o som com base nisso
