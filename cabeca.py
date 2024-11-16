from pybricks.hubs import PrimeHub

from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Side, Direction, Button, Color

from pybricks.tools      import wait, StopWatch
from pybricks.robotics   import DriveBase

from lib.bipes     import bipe_calibracao, bipe_cabeca, musica_vitoria, musica_derrota
from lib.caminhos  import achar_movimentos, tipo_movimento, posicao_desembarque_adulto
from lib.polyfill  import Enum

from micropython import const

from urandom import choice

import cores
import gui
import bluetooth as blt

#! colocar em outro módulo
LOG_LEVEL = Enum("LOG_LEVEL",
    ["NENHUM", "DEBUG", "INFO", "MOVIMENTO", "CORES", "TUDO"]
)
DEBUG = LOG_LEVEL.TUDO

def void(*_, **kw_): return None
debug = log_info = log_mov = log_cor = void

if DEBUG >= LOG_LEVEL.DEBUG:
    debug    = print
if DEBUG >= LOG_LEVEL.INFO:
    log_info = print
if DEBUG >= LOG_LEVEL.MOVIMENTO:
    log_mov  = print
if DEBUG >= LOG_LEVEL.CORES:
    log_cor  = print

TAM_BLOCO   = const(300)
TAM_BLOCO_Y = const(294) # na nossa arena os quadrados não são 30x30cm (são 29.4 por quase 30)

TAM_FAIXA = const(30)
TAM_FAIXA_AZUL = const(60)
TAM_BLOCO_BECO = const(TAM_BLOCO_Y - TAM_FAIXA) # os blocos dos becos são menores por causa do vermelho

PISTA_TODA = const(TAM_BLOCO*6)

DIST_EIXO_SENSOR    = const(80) #mm
DIST_EIXO_SENS_DIST = const(45) #mm   #! checar

DIST_PASSAGEIRO_RUA = const(220) #! checar


#! checar stall ou parado (usar imu) quando não devia: jogar exceção
#! checar cor errada no azul
#! tem um lugar começo do achar azul que tem que dar ré
#! mudar vários debugs pra esses logs novos
#! provavelmente mudar andar_ate pra receber uma fn -> bool e retornar só bool, dist (pegar as informações extras na própria função chamante)
#! fazer posição_estimada/caminho_percorrido_estimado e usar isso pra ter as possibilidades de onde tá
#! talvez usar sensor de cor pra detectar obstáculo de frente (mecanicamente talvez não funcione(muito longe))
#! dá pra usar o sensor de pressão pra detectar o obstáculo
#! fazer módulo movimento/andar_até
#! explorar se faz sentido usar async/await

#! fazer função de calibração com todos os componentes do hsv (talvez fazer dist euclid e usar pesos)

#! colocar mais peso na frente, talvez mudar as coisas de lugar fisicamente

#! ele perde a orientação no alinhar, precisa guardar o quanto ele girou pra cada lado (uma espécie orientação fracionária, se pensar bem) (NSLO, ang)


def setup():
    global hub, rodas, relogio_global
    global sensor_cor_esq, sensor_cor_dir, sensor_ultra_esq, sensor_ultra_dir
    global botao_calibrar, orientacao_estimada
    global rodas_conf_padrao, vels_padrao, vel_padrao, vel_ang_padrao #! fazer um dicionário e concordar com mudar_velocidade
    
    orientacao_estimada = ""
    hub = PrimeHub(broadcast_channel=blt.TX_CABECA, observe_channels=[blt.TX_BRACO])
    log_info(f"spike: {hub.system.name()}")
    while hub.system.name() != "spike1":
        hub.speaker.beep(frequency=1024)
        wait(200)
    else:
        hub.light.blink(Color.RED, [100,50,200,100])

    hub.display.orientation(Side.BOTTOM)
    hub.system.set_stop_button((Button.CENTER, Button.BLUETOOTH))

    sensor_cor_esq = ColorSensor(Port.D)
    sensor_cor_dir = ColorSensor(Port.C)

    sensor_ultra_esq = UltrasonicSensor(Port.F)
    sensor_ultra_dir = UltrasonicSensor(Port.E)

    roda_esq = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE)
    roda_dir = Motor(Port.A, positive_direction=Direction.CLOCKWISE)

    rodas = DriveBase(roda_esq, roda_dir,
                      wheel_diameter=88, axle_track=145.5) #! ver depois se recalibrar

    botao_calibrar = Button.CENTER

    rodas_conf_padrao = rodas.settings() #! CONSTANTIZAR + colocar como um dicionário + usar no mudar_velocidade

    vel_padrao     = rodas_conf_padrao[0]
    vel_ang_padrao = rodas_conf_padrao[2]
    accel_padrao     = rodas_conf_padrao[1]
    accel_ang_padrao = rodas_conf_padrao[3]

    vels_padrao = vel_padrao, vel_ang_padrao

    rodas.settings(vel_padrao*70//40,
                   accel_padrao,
                   vel_ang_padrao*70//40,
                   accel_ang_padrao) #! pus velocidade máxima

    relogio_global = StopWatch()

    return hub

class mudar_velocidade():
    """
    gerenciador de contexto (bloco with) para (automaticamente):
    1. mudar a velocidade do robô
    2. restaurar a velocidade do robô
    """
    def __init__(self, rodas, vel, vel_ang=None): 
        self.rodas = rodas
        self.vel   = vel
        self.vel_ang = vel_ang
 
    def __enter__(self): 
        self.conf_anterior = self.rodas.settings()
        [_, *conf_resto]   = self.conf_anterior
        if self.vel_ang:
            conf_resto[1] = self.vel_ang
        self.rodas.settings(self.vel, *conf_resto)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.rodas.settings(*self.conf_anterior)

def inverte_orientacao():
    global orientacao_estimada
    if   orientacao_estimada == "N": orientacao_estimada = "S"
    elif orientacao_estimada == "S": orientacao_estimada = "N"
    elif orientacao_estimada == "L": orientacao_estimada = "O"
    elif orientacao_estimada == "O": orientacao_estimada = "L"
    else:
        debug(f"inverte_orientação {orientacao_estimada}")
        assert False

def ler_ultrassons():
    return sensor_ultra_esq.distance(), sensor_ultra_dir.distance()

def dar_meia_volta():
    inverte_orientacao()
    rodas.turn(180)
    
def virar_direita(): #! checar a distância aqui e retornar se foi ou tem obstáculo
    global orientacao_estimada
    if   orientacao_estimada == "N": orientacao_estimada = "L"
    elif orientacao_estimada == "O": orientacao_estimada = "N"
    elif orientacao_estimada == "S": orientacao_estimada = "O"
    elif orientacao_estimada == "L": orientacao_estimada = "S"

    log_info(f"virar_direita: {orientacao_estimada=}")
    rodas.turn(90)

def virar_esquerda(): #! checar a distância aqui e retornar se foi ou tem obstáculo
    global orientacao_estimada
    if   orientacao_estimada == "N": orientacao_estimada = "O"
    elif orientacao_estimada == "O": orientacao_estimada = "S"
    elif orientacao_estimada == "S": orientacao_estimada = "L"
    elif orientacao_estimada == "L": orientacao_estimada = "N"

    log_info(f"virar_esquerda: {orientacao_estimada=}")
    rodas.turn(-90)

def mudar_orientação(ori_final):
    log_info(f"mudar_orientacao: {orientacao_estimada} a {ori_final}")
    while orientacao_estimada != ori_final:
        virar_esquerda()
        debug(f"mudar_orientacao: indo {orientacao_estimada} a {ori_final}")

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

def dar_re_meio_bloco(eixo_menor=False):
    if eixo_menor:
        dar_re(TAM_BLOCO_Y//2 - DIST_EIXO_SENSOR)
    else:
        dar_re(TAM_BLOCO//2   - DIST_EIXO_SENSOR)

def ver_nao_pista() -> tuple[bool, tuple[Color, hsv], tuple[Color, hsv]]: # type: ignore
    #! usar verificar_cor em vez disso?
    esq, dir = cores.todas(sensor_cor_esq, sensor_cor_dir)
    return ((not cores.pista_unificado(*esq) or not cores.pista_unificado(*dir)),
            esq, dir)

def ver_azul_lado():
    esq, dir = cores.todas(sensor_cor_esq, sensor_cor_dir)
    return ((cores.azul_unificado(*esq) ^ cores.azul_unificado(*dir)),
            esq, dir)

def verificar_cor(func_cor) -> Callable[None, tuple[bool, int]]: # type: ignore
    def f():
        esq, dir = cores.todas(sensor_cor_esq, sensor_cor_dir)
        return (func_cor(*esq) or func_cor(*dir), esq, dir)
    return f

def ver_passageiro_perto():
    #log_info("ver_passageiro_perto")
    dist_esq, dist_dir = ler_ultrassons()
    return ((dist_esq < DIST_PASSAGEIRO_RUA or dist_dir < DIST_PASSAGEIRO_RUA),
            dist_esq, dist_dir)

def nao_ver_passageiro_perto():
    #log_info("nao_ver_passageiro_perto")
    dist_esq, dist_dir = ler_ultrassons()
    return ((dist_esq < DIST_PASSAGEIRO_RUA and dist_dir < DIST_PASSAGEIRO_RUA),
            dist_esq, dist_dir)

def andar_ate_idx(*conds_parada: Callable, dist_max=PISTA_TODA) -> tuple[bool, tuple[Any]]: # type: ignore
    log_info("andar_ate:")
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

nunca_parar   = (lambda: (False, False))
ou_manter_res = (lambda res, ext: (res, ext))

def andar_ate_bool(sucesso, neutro=nunca_parar, fracasso=ver_nao_pista,
                            ou=ou_manter_res, dist_max=PISTA_TODA):
    succ, neut, frac = 1, 2, 3
    while True:
        res, extra = andar_ate_idx(sucesso, neutro, fracasso,
                                   dist_max=dist_max)

        if   res == succ: return True, extra
        elif res == frac: return False, extra
        elif res == neut: continue
        elif res == 0:
            debug("andar_ate_cor: andou demais")
            return False, (None,) #ou(res, extra)
        else: 
            debug(f"andar_ate_cor: {res}")
            assert False

def alinha_limite(max_tentativas=3):
    for i in range(max_tentativas):
        rodas.reset()
        dar_re_meio_bloco()
        alinhou = alinha_parede(vel=80, vel_ang=30, giro_max=70)
        ang  = rodas.angle()
        dist = rodas.distance()
        if alinhou: return
        else:
            with mudar_velocidade(rodas, 80, 30):
                rodas.turn(-ang)
                dar_re(dist)
                rodas.turn(ang)
    return

def achar_limite() -> tuple[tuple[Color, hsv], tuple[Color, hsv]]: # type: ignore
    achou, extra = andar_ate_idx(ver_nao_pista)
    if achou:
        return extra
    else:
        return cores.todas(sensor_cor_esq, sensor_cor_dir)

def achar_azul() -> bool:
    esq, dir = achar_limite(); alinha_limite() # anda reto até achar o limite

    if cores.beco_unificado(*esq) or cores.beco_unificado(*dir): #! beco é menor que os outros blocos
        log_info(f"achar_azul: beco")

        dar_re_meio_bloco()
        dar_re(TAM_BLOCO_BECO) 

        choice((virar_direita, virar_esquerda))() # divertido

        #! lidar com os casos de cada visto (andar_ate[...])
        esq, dir = achar_limite(); alinha_limite() # anda reto até achar o limite
        log_info(f"achar_azul: beco indo azul") 

        if cores.parede_unificado(*esq) or cores.parede_unificado(*dir): dar_meia_volta()

        #! lidar com os casos de cada visto (andar_ate[...])
        esq, dir = achar_limite() # anda reto até achar o limite #! alinha?
        log_info(f"achar_azul: beco indo azul certeza")

        if cores.certificar(sensor_cor_esq, sensor_cor_dir, cores.azul_unificado):
            return True
        else:
            alinha_limite()
            return cores.certificar(sensor_cor_esq, sensor_cor_dir, cores.azul_unificado)
    elif cores.parede_unificado(*esq) or cores.parede_unificado(*dir):
        log_info(f"achar_azul: parede")

        dar_re_meio_bloco()
        choice((virar_direita, virar_esquerda))() # divertido      

        return False
    else: #azul
        log_info("achar_azul: vi azul")
        #! deixar mais andar_ate(ver_azul, ver_nao_branco) switch()
        esq, dir = achar_limite() # anda reto até achar o limite #! alinha?

        if cores.certificar(sensor_cor_esq, sensor_cor_dir, cores.azul_unificado):
            log_info("achar_azul: azul mesmo")
            dar_re(TAM_BLOCO_BECO*3//8)
            return True
        else:
            log_info("achar_azul: não azul")
            dar_re_meio_bloco()
            choice((virar_direita, virar_esquerda))() #!
            return False

def alinha_parede(vel, vel_ang, giro_max=45) -> bool: #! avaliar giro_max
    alinhado_nao_pista = (lambda esq, dir: not cores.pista_unificado(*esq) and not cores.pista_unificado(*dir))
    desalinhado_esq    = (lambda esq, dir: not cores.pista_unificado(*esq) and     cores.pista_unificado(*dir))
    desalinhado_dir    = (lambda esq, dir: not cores.pista_unificado(*dir) and     cores.pista_unificado(*esq))
    alinhado_pista     = (lambda esq, dir:     cores.pista_unificado(*esq) and     cores.pista_unificado(*dir))

    with mudar_velocidade(rodas, vel, vel_ang):
        parou, extra = andar_ate_idx(ver_nao_pista, dist_max=TAM_BLOCO//2)
        if not parou:
            (dist,) = extra
            debug(f"alinha_parede: reto branco {dist}")
            return False # viu só branco, não sabemos se tá alinhado
    
        (dir, esq) = extra
        if  alinhado_nao_pista(esq, dir):
            debug("alinha_parede: reto não pista")
            return True
        elif desalinhado_dir(esq, dir):
            debug("alinha_parede: torto pra direita")
            GIRO = -giro_max
        elif desalinhado_esq(esq, dir):
            debug("alinha_parede: torto pra esquerda")
            GIRO = giro_max

        rodas.turn(GIRO, wait=False) #! fazer gira_ate
        while not rodas.done():
            esq, dir = cores.todas(sensor_cor_esq, sensor_cor_dir)
            if  alinhado_nao_pista(esq, dir):
                debug("alinha_parede: alinhado parede")
                parar_girar()
                return True # deve tar alinhado
            elif alinhado_pista(esq, dir):
                debug("alinha_parede: alinhado pista")
                parar_girar()
                return False #provv alinhado, talvez tentar de novo

            if relogio_global.time() % 100 == 0:
                log_cor(f"alinha_parede: desalinhado {esq}, {dir}")
        return False # girou tudo, não sabemos se tá alinhado

def alinhar(max_tentativas=4, virar=True, vel=80, vel_ang=20, giro_max=70) -> None:
    for _ in range(max_tentativas): #! esqueci mas tem alguma coisa
        rodas.reset()
        alinhou = alinha_parede(vel, vel_ang, giro_max=giro_max)

        ang  = rodas.angle()
        dist = rodas.distance()
        with mudar_velocidade(rodas, vel, vel_ang):
            rodas.turn(-ang)
            dar_re(dist)
            rodas.turn(ang)

        if alinhou: return
        else:
            if virar: virar_direita() #! testar agora
            continue
    return
        

def pegar_passageiro() -> bool:
    global orientacao_estimada

    log_info("pegar_passageiro:")
    with mudar_velocidade(rodas, 50):
        res, info = andar_ate_idx(ver_passageiro_perto,
                                  verificar_cor(cores.beco_unificado),
                                  #! verificar_cor(cores.parede_unificado),
                                  dist_max=TAM_BLOCO*4)
        if res == 1:
            (dist_esq, dist_dir) = info
            if dist_esq < dist_dir:
                dist = dist_esq
                virar, desvirar = virar_esquerda, virar_direita
            else:
                dist = dist_dir
                virar, desvirar = virar_direita, virar_esquerda

            blt.abrir_garra(hub)
            with mudar_velocidade(rodas, *vels_padrao):
                dar_re(DIST_EIXO_SENS_DIST-20) #! desmagificar
                virar()
                andar_ate_bool(verificar_cor(cores.azul_unificado), dist_max=70) #! desmagificar
                rodas.straight(min(dist, TAM_FAIXA_AZUL+10))
                blt.fechar_garra(hub)
            cor_cano = blt.ver_cor_passageiro(hub)
            log_info(f"pegar_passageiro: cor_cano {cores.cor(cor_cano)}")

            if cor_cano == cores.cor.BRANCO: 
                with mudar_velocidade(rodas, *vels_padrao):
                    blt.abrir_garra(hub)
                    dar_re(min(dist, TAM_FAIXA_AZUL+10))
                    desvirar()
                    rodas.straight(TAM_BLOCO//4) #! desmagi
                return False
            elif cor_cano == cores.cor.NENHUMA: #!
                with mudar_velocidade(rodas, *vels_padrao):
                    dar_re(20) #! desmagi
                    blt.abrir_garra(hub)
                    dar_re(min(dist, TAM_FAIXA_AZUL+10))
                    blt.resetar_garra(hub)
                    desvirar()
                    #dar_re(20) #! desmagi
                return False
            return True
        elif res == 2:
            (cor_esq, cor_dir) = info
            log_cor(f"pegar_passageiro: vermelho {cor_esq=}, {cor_dir=}")
            with mudar_velocidade(rodas, *vels_padrao):
                dar_re_meio_bloco()
                dar_meia_volta()

            return False # é pra ter chegado no vermelho
        elif res == 3:
            (cor_esq, cor_dir) = info
            log_cor(f"pegar_passageiro: parede {cor_esq=}, {cor_dir=}")
            with mudar_velocidade(rodas, *vels_padrao):
                dar_re_meio_bloco()
                dar_meia_volta()

            return False #! falhar mais alto
        else:
            log_info(f"pegar_passageiro: andou muito {rodas.distance()}")
            with mudar_velocidade(rodas, *vels_padrao):
                dar_re_meio_bloco()
                dar_meia_volta()

            return False # chegou na distância máxima

def pegar_primeiro_passageiro() -> Color:
    global orientacao_estimada

    log_info("pegar_primeiro_passageiro:")
    #! a cor é pra ser azul
    virar_direita()
    deu, _ = andar_ate_bool(sucesso=verificar_cor(cores.beco_unificado),
                            fracasso=verificar_cor(cores.parede_unificado))
    while not deu: #! fazer com exceção aqui
        deu, _ = andar_ate_bool(sucesso=verificar_cor(cores.beco_unificado),
                                fracasso=verificar_cor(cores.parede_unificado))

    dar_re_meio_bloco()
    dar_meia_volta()

    pegou = False
    while not pegou: pegou = pegar_passageiro()
    
    return blt.ver_cor_passageiro(hub)

def interpretar_movimento(mov): #! talvez lidar com coisas novas enquanto tiver aqui
    if   mov == tipo_movimento.FRENTE:
        rodas.straight(TAM_BLOCO, then=Stop.COAST)
    elif mov == tipo_movimento.TRAS:
        dar_meia_volta()
        rodas.straight(TAM_BLOCO, then=Stop.COAST)
    elif mov == tipo_movimento.ESQUERDA_FRENTE:
        virar_esquerda()
        rodas.straight(TAM_BLOCO, then=Stop.COAST)
    elif mov == tipo_movimento.DIREITA_FRENTE:
        virar_direita()
        rodas.straight(TAM_BLOCO, then=Stop.COAST)
    elif mov == tipo_movimento.ESQUERDA:
        virar_esquerda()
    elif mov == tipo_movimento.DIREITA:
        virar_direita()

def interpretar_caminho(caminho): #! receber orientação?
    for mov in caminho: #! yield orientação nova?
        debug(f"interpretar_caminho: {tipo_movimento(mov)}")
        interpretar_movimento(mov)
        yield rodas.distance()

def seguir_caminho(pos, obj): #! lidar com outras coisas
    movs, ori_final, pos_fim = achar_movimentos(pos, obj, orientacao_estimada)

    for _ in interpretar_caminho(movs):
        while not rodas.done(): pass
    
    mudar_orientação(ori_final)

    return pos_fim

def seguir_caminho_contrario(pos, obj):
    _   , ori_final, pos_final = achar_movimentos(pos,       obj, orientacao_estimada)
    movs, _,         pos_final = achar_movimentos(pos_final, pos, ori_final)

    for _ in interpretar_caminho(movs):
        while not rodas.done(): pass
    
    return pos_final

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


def main():
    global orientacao_estimada

    crono = StopWatch()
    while crono.time() < 100: #! ativar calibração quando for usar
        botões = hub.buttons.pressed()
        if botao_calibrar in botões:
            bipe_calibracao(hub)
            #! levar os dois sensores em consideração separadamente
            mapa_hsv = menu_calibracao(hub, sensor_cor_esq, sensor_cor_dir)
            cores.repl_calibracao(mapa_hsv)
            return

    hub.system.set_stop_button((Button.BLUETOOTH,))
    while True:
        bipe_cabeca(hub)
        blt.resetar_garra(hub)

        """
        #! antes de qualquer coisa, era bom ver se na sua frente tem obstáculo
        #! sobre isso ^ ainda, tem que tomar cuidado pra não confundir eles com os passageiros
        achou_azul = False
        alinhar()
        while not achou_azul:
            achou_azul = achar_azul()
        debug(f"main: {orientacao_estimada=}") #assert ori == "L"
        """
        achar_limite(); alinha_limite() #! teste agora
        orientacao_estimada = "L"
        cor = pegar_primeiro_passageiro()

        achar_limite(); alinha_limite() #! lidar com os casos de cada visto (andar_ate[...])

        #! comprimir esses ifs com com posicao_desembarque_adulto.get()
        #! verificar tamanho do passageiro e funcao p verificar se desembarque disponivel
        if   cor == cores.cor.VERDE:    fim = posicao_desembarque_adulto['VERDE']
        elif cor == cores.cor.VERMELHO: fim = posicao_desembarque_adulto['VERMELHO']
        elif cor == cores.cor.AZUL:     fim = posicao_desembarque_adulto['AZUL']
        elif cor == cores.cor.MARROM:   fim = posicao_desembarque_adulto['MARROM'] #! fazer acontecer
        else: #! marrom
            fim = posicao_desembarque_adulto['MARROM']
            debug(f"main: {cores.cor(cor)}")
            assert False

        dar_re(TAM_BLOCO//3) #! desmagificar
        choice((virar_esquerda, virar_direita))()
        achar_limite(); alinha_limite() #! lidar com os casos de cada visto (andar_ate[...])
        #! aqui é pra ser vermelho
        dar_re_meio_bloco()

        if   orientacao_estimada == "N": pos = (0,5)
        elif orientacao_estimada == "S": pos = (4,5)
        else:
            log_info(f"main: {orientacao_estimada=}")
            assert False

        seguir_caminho(pos, fim)

        rodas.straight(TAM_BLOCO//2)
        blt.abrir_garra(hub)
        dar_re(TAM_BLOCO//2)

        seguir_caminho_contrario(pos, fim)