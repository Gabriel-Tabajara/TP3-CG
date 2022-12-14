# ***********************************************************************************
#   OpenGLBasico3D-V5.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
# 
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# 
# ***********************************************************************************
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
import Objeto3d
import numpy as np
from PIL import Image
from Bezier import Bezier
import time

corAtual = 0
cores = [
    (0, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1),
    (0.5, 0.5, 0.5),
    (0, 0, 0)
]

bezier = Bezier(Ponto(0,0,0), Ponto(0,15,15), Ponto(0,0,30))

image = None
texturas = []
angulo = 0.0
zoom = 1
look_x = 5
look_y = 1
look_z = -5

FORCA = 25

travado = False

angle = 60.0
obs_x = 9.5
obs_z = 2.4
obs_y = 0
lx =  math.sin(angle)
lz = -math.cos(angle)

atirando = False

tanque_x = 0
tanque_z = 0
anguloTanque = 0
lxTanque =  math.sin(anguloTanque)
lzTanque =  math.cos(anguloTanque) 
mudou = False
girou = False


articulacao_1 = -45
articulacao_2 = 0

cactus = Objeto3d.Tri("./objects/cactus.tri")
casa = Objeto3d.Tri("./objects/casa.tri")
moto = Objeto3d.Tri("./objects/moto.tri")
dog = Objeto3d.Tri("./objects/dog.tri")
ferrari = Objeto3d.Tri("./objects/ferrari.tri")
vaca = Objeto3d.Tri("./objects/vaca.tri")
tree = Objeto3d.Tri("./objects/tree.tri")
tree_1 = Objeto3d.Tri("./objects/tree_1.tri")

cachorros = [(0,1,35,.3), (15,1,28,.5), (10,1,45,.4), (0,1,28,.3), (17,1,29,.3)]

parede = []
for x in range(0, 25):
    linha = []
    for y in range(0, 15):
        linha.append(True)
    parede.append(linha)

# ***********************************************
def calculaPonto(p: Ponto) -> Ponto:
    
    ponto_novo = [0,0,0,0]
    
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    for i in range(0, 4):
        ponto_novo[i] = mvmatrix[0][i] * p.x + \
                        mvmatrix[1][i] * p.y + \
                        mvmatrix[2][i] * p.z + \
                        mvmatrix[3][i]

    x = ponto_novo[0]
    y = ponto_novo[1]
    z = ponto_novo[2]
    #print ("Ponto na saida:")
    #print (ponto_novo)
    return Ponto(x, y, z)


# **********************************************************************
def loadTexture(nome) -> int:
    global image
    # carrega a imagem
    image = Image.open(nome)
    # print ("X:", image.size[0])
    # print ("Y:", image.size[1])
    # converte para o formato de OpenGL 
    img_data = np.array(list(image.getdata()), np.uint8)

    # Habilita o uso de textura
    glEnable ( GL_TEXTURE_2D )

    #Cria um ID para texura
    texture = glGenTextures(1)
    errorCode =  glGetError()
    if errorCode == GL_INVALID_OPERATION: 
        print ("Erro: glGenTextures chamada entre glBegin/glEnd.")
        return -1

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Define que tipo de textura ser usada
    # GL_TEXTURE_2D ==> define que ser· usada uma textura 2D (bitmaps)
    # e o nro dela
    glBindTexture(GL_TEXTURE_2D, texture)

    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    errorCode = glGetError()
    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # neste ponto, "texture" tem o nro da textura que foi carregada
    errorCode = glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glTexImage2D chamada entre glBegin/glEnd.")
        return -1

    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1
    #image.show()
    return texture

# **********************************************************************
#  Habilita o uso de textura 'NroDaTextura'
#  Se 'NroDaTextura' <0, desabilita o uso de texturas
#  Se 'NroDaTextura' for maior que a quantidade de texturas, gera
#  mensagem de erro e desabilita o uso de texturas
# **********************************************************************
def useTexture (NroDaTextura: int):
    global texturas
    if (NroDaTextura>len(texturas)):
        print ("Numero invalido da textura.")
        glDisable (GL_TEXTURE_2D)
        return
    if (NroDaTextura < 0):
        glDisable (GL_TEXTURE_2D)
    else:
        glEnable (GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texturas[NroDaTextura])

# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(0.5, 0.5, 1, 1.0)

    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    # glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Carrega texturas
    global texturas 
    texturas += [loadTexture("bricks.jpg")] 
    texturas += [loadTexture("Piso.jpg")] 
    texturas += [loadTexture("metal.jpg")] 
# **********************************************************************
#
# **********************************************************************
soltou = False
cam = 0
def posicUser():
    global zoom, look_x, look_y, look_z, obs_z, obs_x, obs_y, lz, lx, travado, angle
    global soltou, cam
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(60,AspectRatio,0.01,5000) # Projecao perspectiva

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # print(travado)
    if not travado:
        gluLookAt(obs_x,       look_y,        obs_z,
                  obs_x+lx*10, look_y+obs_y,  obs_z+lz*10,
                0,1.0,0)
    else:
        soltou = True
        if cam == 1:
            gluLookAt(  12.5,    look_y+5,  -13,
                        12.5,    look_y,  50,
                        0,1.0,0)
        elif cam == 2:
            gluLookAt(  -25,    look_y+10,  25,
                        50,    look_y,    25,
                        0,1.0,0)


 
# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
	# Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "posicUser".
    AspectRatio = w / h
	# Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)
    
    posicUser()

# **********************************************************************
def defineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente =    [0.4, 0.4, 0.4] 
    LuzDifusa   =    [0.7, 0.7, 0.7]
    LuzEspecular =   [0.9, 0.9, 0.9]
    PosicaoLuz0  =   [2.0, 3.0, 0.0]  # Posicao da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    # Habilita o uso de iluminacao
    glEnable(GL_LIGHTING)

    # Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz numero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentracao do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serah o brilho. (Valores validos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)

# **********************************************************************
# desenhaCubo()
# Desenha o cenario
# **********************************************************************
def desenhaCubo():
    glutSolidCube(1)

def desenhaCilindro():
    glutSolidCylinder(
        0.5,1,20,20
    )

def desenhaBala(x,y,z):
    glPushMatrix()
    glTranslate(x,y,z)
    glutSolidSphere(0.5,20,20)
    glPopMatrix()
# **********************************************************************
# void desenhaLadrilho(int corBorda, int corDentro)
# Desenha uma celula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e esta' sobre o plano XZ
# **********************************************************************
def desenhaLadrilho():
    glColor3f(1,1,1) # desenha QUAD em branco, pois vai usa textura
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(0,0)
    glVertex3f(-0.5,  0.0 , -0.5)
    glTexCoord(0,1)
    glVertex3f(-0.5,  0.0,  0.5)
    glTexCoord(1,1)
    glVertex3f( 0.5,  0.0,  0.5)
    glTexCoord(1,0)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()
    
    glColor3f(1,1,1) # desenha a borda da QUAD 
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()

def desenhaLadrilhoParede(ponto:Ponto):
    global cores
    r,g,b = cores[int(ponto.x + ponto.y)%len(cores)]
    glColor3f(r,g,b) # desenha QUAD em branco, pois vai usa textura
    glBegin ( GL_QUADS )
    glNormal3f(0,0,1)
    glTexCoord(0,0)
    glVertex3f(ponto.x-0.5,  ponto.y-0.5 , ponto.z-0.0)
    glTexCoord(0,1)
    glVertex3f(ponto.x+0.5,  ponto.y-0.5,  ponto.z-0.0)
    glTexCoord(1,1)
    glVertex3f(ponto.x+0.5,  ponto.y+0.5,  ponto.z+0.0)
    glTexCoord(1,0)
    glVertex3f(ponto.x-0.5,  ponto.y+0.5,  ponto.z+0.0)
    glEnd()
    
    glColor3f(0,1,0) # desenha a borda da QUAD
    glLineWidth(3)
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,0,1)
    glVertex3f(ponto.x-0.5,  ponto.y-0.5, ponto.z-0.0)
    glVertex3f(ponto.x-0.5,  ponto.y+0.5, ponto.z+0.0)
    glVertex3f(ponto.x+0.5,  ponto.y+0.5, ponto.z+0.0)
    glVertex3f(ponto.x+0.5,  ponto.y-0.5, ponto.z-0.0)
    glEnd()
    

# **********************************************************************
def desenhaParede():
    global parede
    for x in range(len(parede)):
        for y in range(len(parede[x])):
            ponto = parede[x][y]
            if not ponto: continue
            useTexture(-1)
            desenhaLadrilhoParede(Ponto(x,y,25))

def desenhaPiso():
    glPushMatrix()
    glTranslated(0,0,0)
    for x in range(0, 25):
        glPushMatrix()
        for z in range(0, 50):
            if z%2==0:
                useTexture(0)
            else:
                useTexture(1)
            desenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()


passos = 0
bezierTiro = None
jaPegou = False
pontoOriginal1 = Ponto()
pontoOriginal2 = Ponto()
pontoOriginal3 = Ponto()
newBezier = None
oldAngle = 0
diferenca = (0,0)
def desenharTanque():
    global tanque_x, tanque_z, anguloTanque, articulacao_1, articulacao_2, FORCA, atirando, bezierTiro, passos, jaPegou, newBezier
    global pontoOriginal1, pontoOriginal2, pontoOriginal3
    global parede
    global girou, oldAngle, diferenca
    if not girou: oldAngle = anguloTanque
        
    glPushMatrix()
    glColor(.5,.5,1)
    glTranslatef(tanque_x, 0.5, tanque_z)
    glRotatef(anguloTanque, 0, 1, 0)
    desenhaCubo()
    glTranslatef(1,0,0)
    desenhaCubo()
    glTranslatef(0,0,1)
    desenhaCubo()
    glTranslatef(-1,0,0)
    desenhaCubo()
    glTranslatef(0,0,1)
    desenhaCubo()
    glTranslatef(1,0,0)
    desenhaCubo()
    
    useTexture(-2)
    radTanque = anguloTanque * math.pi/180
    rad = articulacao_1 * math.pi/180
    bX = 0
    bY = -math.sin(rad)
    bZ = math.cos(rad)

    bX = -.5
    bY = bY*FORCA
    bZ = bZ*FORCA

    # useTexture(-1)
    glPushMatrix()
    glTranslate(0,.25,0)
    bezier = Bezier(Ponto(bX,0,0), Ponto(bX, bY, bZ), Ponto(bX,0,bZ*2))

    glPopMatrix()
    
    glPushMatrix()
    glColor(1,0,0)
    glTranslatef(-1.05,-0.5,-2)
    glRotatef(articulacao_1,1,0,0)
    glPushMatrix()
    glScalef(0.3,0.3,2)
    desenhaCilindro()
    glPopMatrix()
    
    glColor(1,1,0)
    glTranslatef(0,0,0.8)
    glRotatef(articulacao_2,1,0,0)
    glPushMatrix()
    glScalef(0.16,0.16,2)
    desenhaCilindro()
    glPopMatrix()
    glRotatef(270,0,0,1)
    glRotatef(90,1,0,0)
    glPopMatrix()
    glPopMatrix()

    if not jaPegou:
        tX = tanque_x
        tY = (-math.sin(rad)) * FORCA
        tZ = tanque_z + math.cos(rad)*FORCA
        pontoOriginal1 = Ponto(tanque_x, 0, tanque_z)

        meio = Ponto(tX, 0, tZ)

        vet = meio - pontoOriginal1
        modulo = vet.modulo()

        posX = math.sin(radTanque)
        posZ = math.cos(radTanque)

        posX = posX * modulo
        posZ = posZ * modulo

        pontoOriginal2 = Ponto(posX + tanque_x, tY, posZ + tanque_z)
        pontoOriginal3 = Ponto(posX*2 + tanque_x, 0, posZ*2 + tanque_z)

        bezierTiro = Bezier(pontoOriginal1, pontoOriginal2, pontoOriginal3)

    if atirando:
        jaPegou = True
        atira(bezierTiro)
        
    else: passos = 0
    if bezierTiro: 
        bezierTiro.Traca()

acertou = False
def atira(bezier: Bezier):
    global passos, jaPegou, atirando, acertou, cachorros
    posicao = bezier.Calcula(passos)
    if posicao.z > 24 and posicao.z < 26 and not acertou:
        acertou = destroiParede(posicao.x, posicao.y)
    for i in range(len(cachorros)):
        cachorro = cachorros[i]
        if cachorro == None: continue
        x,y,z,scale = cachorro
        if dog.colision(posicao.x, posicao.y, posicao.z, x, y, z, scale):
            acertou = True
            atirando = False
            cachorros[i] = None
    desenhaBala(posicao.x, posicao.y, posicao.z)
    passos += 0.025
    if passos > 1.05 or acertou:
        atirando = False
        jaPegou = False
        acertou = False

def destroiParede(x, y):
    global parede
    x,y = int(x), int(y)
    if not isValid(x, y): return False
    acertou = parede[x][y]
    if not acertou: return False
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if isValid(x+i, y+j):
                print(x+i, y+j)
                parede[x+i][y+j] = False
    return True

def isValid(x, y):
    global parede
    if x < 0 or x >= len(parede): return False
    if y < 0 or y >= len(parede[0]): return False
    return True

# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
# **********************************************************************
def display():
    global angulo
    global pos_x, pos_y, pos_z
    global tanque_z
    global look_x, look_y, look_z
    global dog, cachorros
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    defineLuz()
    posicUser()
    # for i in range(0,20):
    #     glPushMatrix()
    #     glTranslatef(1.5*i + 13,0,42)
    #     glScalef(0.3,0.3,0.3)
    #     drawObj(dog)
    #     glScalef(2,2,2)
    #     glPopMatrix()
    
    for cachorro in cachorros:
        if cachorro == None: continue
        glPushMatrix()
        x,y,z,scale = cachorro
        glTranslatef(x, y, z)
        glScalef(scale,scale,scale)
        drawObj(dog)
        glPopMatrix()


    glMatrixMode(GL_MODELVIEW)
    
    desenhaPiso()
    desenhaParede()
    desenharTanque()

    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais

nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        # print(nFrames)
        nFrames = 0
        glutPostRedisplay()
    

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global zoom, look_x, look_z, lx, angle, lz, obs_x, obs_z
    global tanque_x, tanque_z, anguloTanque, lxTanque, lzTanque
    global mudou, girou
    global articulacao_1, articulacao_2
    global atirando, travado, cam
    global FORCA
    #print (args)
    calculaAngulo = False
    # If escape is pressed, kill everything.
    print(args[0])
    if args[0] == b'1':
        cam = 1
        travado = True
    if args[0] == b'2':
        cam = 2
        travado = True
    
    if args[0] == b'3':
        travado = False
        # cam = 0


    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada
    if args[0] == b'q':
        FORCA += 1
    if args[0] == b'e':
        FORCA -= 1
    if args[0] == b'w':
        obs_x += lx 
        obs_z += lz 
    if args[0] == b's':
        obs_x -= lx 
        obs_z -= lz
    if args[0] == b'a':
        articulacao_1 += 2
    if args[0] == b'd':
        articulacao_1 -= 2
    if args[0] == b'b':
        articulacao_2 += 2
        pass
    if args[0] == b'B':
        articulacao_2 -= 2
    if args[0] == b' ':
        atirando = True
    if args[0] == b't':
        tanque_z += 0.18*lzTanque
        tanque_x += 0.18*lxTanque
    if args[0] == b'g':
        tanque_z -= 0.18*lzTanque
        tanque_x -= 0.18*lxTanque
    if args[0] == b'f':
        anguloTanque += 1
        calculaAngulo = True
        girou = True
    if args[0] == b'h':
        anguloTanque -= 1
        calculaAngulo = True
        girou = True
        

    if calculaAngulo:   
        lxTanque =   math.sin(anguloTanque*math.pi/180)
        lzTanque =   math.cos(anguloTanque*math.pi/180)

    if args[0] == b'i':
        image.show()

    # ForÃ§a o redesenho da tela
    glutPostRedisplay()

#**********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global zoom, look_x, look_y, look_z, lx, angle, lz, obs_x, obs_z
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        look_y += 1
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        look_y -= 1
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        angle -= 0.1
        lx =  math.sin(angle)
        lz = -math.cos(angle)
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        angle += 0.1
        lx =  math.sin(angle)
        lz = -math.cos(angle)

    glutPostRedisplay()


start = 0
anteriorX = 0
anteriorY = 0
movendoX = False
movendoY = False
first = True
def mouse(button: int, state: int, x: int, y: int):
    global obs_y, angle, start, movendoX, movendoY, firstX, firstY
    print(x, y, state, button)
    
    if button == 0 and state == 0:
        movendoX = True
        movendoY = True
    if button == 0 and state == 1:
        movendoY = True
        movendoX = False
        firstX = True
    if button == 2 and state == 0:
        movendoY = True
    if button == 2 and state == 1:
        movendoY = False
        firstY = True
    
    print(x, y)
    if button == 3: obs_y += .05
    if button == 4: obs_y -= .05
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    global angle, movendoX, movendoY, anteriorX, anteriorY, start, lx, lz, firstX, firstY, obs_y
    if movendoX:
        if anteriorX == 0 or firstX: anteriorX = x
        firstX = False
        atualX = x
        deltaX = atualX - anteriorX
        angle += deltaX/(1920/2)
        lx =  math.sin(angle)
        lz = -math.cos(angle)
        anteriorX = atualX
    
    if movendoY:
        if anteriorY == 0 or firstY: anteriorY = y
        firstY = False
        atualY = y
        deltaY = atualY - anteriorY
        obs_y -= deltaY/(1080/6)
        anteriorY = atualY


    glutPostRedisplay()
#**********************************************************************

def drawObj(obj:Objeto3d.Tri):
    obj.draw(mask=False)

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_RGB)
glutInitWindowPosition(0, 0)

glutInitWindowSize(1920, 1080)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL 3D & Textures")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutReshapeFunc(reshape)
# glClientWaitSync()
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
glutMotionFunc(mouseMove)



try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
