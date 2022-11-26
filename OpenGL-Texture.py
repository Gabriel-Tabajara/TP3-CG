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
import time

image = None
texturas = []
angulo = 0.0
zoom = 1
look_x = 5
look_y = 1
look_z = -5

angle = 60.0
obs_x = 9.5
obs_z = 2.4
lx =  math.sin(angle)
lz = -math.cos(angle)

tanque_x = 0
tanque_z = 0
anguloTanque = 0
lxTanque =  math.sin(anguloTanque)
lzTanque =  math.cos(anguloTanque) 
mudou = False

articulacao_1 = 0
articulacao_2 = 0

cactus = Objeto3d.Tri("./objects/cactus.tri")
casa = Objeto3d.Tri("./objects/casa.tri")
moto = Objeto3d.Tri("./objects/moto.tri")
dog = Objeto3d.Tri("./objects/dog.tri")

parede = []
parede1 = []
for x in range(0, 25):
    linha = []
    for y in range(0, 15):
        linha.append(Ponto(x, y, 25))
        # parede1.append(Ponto(x,y,0))
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
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Carrega texturas
    global texturas 
    texturas += [loadTexture("bricks.jpg")] 
    texturas += [loadTexture("Piso.jpg")] 
# **********************************************************************
#
# **********************************************************************
def posicUser():
    global zoom, look_x, look_y, look_z, obs_z, obs_x, lz, lx
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(60,AspectRatio,0.01,5000) # Projecao perspectiva

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(obs_x,    look_y,  obs_z,
              obs_x+lx, look_y,  obs_z+lz,
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
    glColor3f(1,1,1) # desenha QUAD em branco, pois vai usa textura
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
    glTranslated(0,0,0)
    global parede
    for linha in parede:
        for ponto in linha:
            ponto:Ponto
            useTexture(-1)
            desenhaLadrilhoParede(ponto)
    for ponto in parede1:
        ponto:Ponto
        useTexture(0)
        desenhaLadrilhoParede(ponto)

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

def desenharTanque():
    global tanque_x, tanque_z, anguloTanque, articulacao_1, articulacao_2
    glPushMatrix()
    glNormal(0,1,0)
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
    
    glPushMatrix()
    glColor(1,0,0)
    glTranslatef(-0.5,0.3,0)
    glRotatef(270 + articulacao_1,1,0,0)
    glPushMatrix()
    glScalef(0.3,0.3,1)
    desenhaCilindro()
    glPopMatrix()
    
    glColor(1,1,0)
    glTranslatef(0,0,0.8)
    glRotatef(articulacao_2,1,0,0)
    glScalef(0.16,0.16,1)
    desenhaCilindro()
    glPopMatrix()
    glPopMatrix()


# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
# **********************************************************************
def display():
    global angulo
    global pos_x, pos_y, pos_z
    global tanque_z
    global look_x, look_y, look_z
    global dog
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    defineLuz()
    posicUser()

    # glPushMatrix()
    # glTranslatef(5,0,35)
    # glScalef(0.1,0.1,0.1)
    # drawObj(cactus)
    # glPopMatrix()
    
    # for i in range(0,20):
    #     glPushMatrix()
    #     glTranslatef(1.5*i + 13,0,42)
    #     glScalef(0.3,0.3,0.3)
    #     drawObj(dog)
    #     glScalef(2,2,2)``
    #     glPopMatrix()
    
    # glPushMatrix()
    # glTranslatef(13,0,42)
    # glScalef(0.3,0.3,0.3)
    # drawObj(dog)
    # glScalef(2,2,2)
    # glPopMatrix()


    glMatrixMode(GL_MODELVIEW)
    

    # glColor3f(0.0,0.5,0.0) # Amarelo
    # glPushMatrix()
    # glTranslatef(look_x, look_y, look_z)
    # desenhaCubo()
    # glPopMatrix()

    desenhaPiso()
    desenhaParede()
    desenharTanque()

    angulo = angulo + 1

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
    global mudou
    global articulacao_1, articulacao_2
    #print (args)
    calculaAngulo = False
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b'w':
        obs_x += lx 
        obs_z += lz 
    if args[0] == b's':
        obs_x -= lx 
        obs_z -= lz
    if args[0] == b'a':
        articulacao_1 += 2
        pass
    if args[0] == b'A':
        articulacao_1 -= 2
        pass
    if args[0] == b'b':
        articulacao_2 += 2
        pass
    if args[0] == b'B':
        articulacao_2 -= 2
        pass
    if args[0] == b'd':
        pass
    if args[0] == b' ':
        init()
    if args[0] == b't':
        tanque_z += 0.18*lzTanque
        tanque_x += 0.18*lxTanque
    if args[0] == b'g':
        tanque_z -= 0.18*lzTanque
        tanque_x -= 0.18*lxTanque
    if args[0] == b'f':
        anguloTanque += 1
        calculaAngulo = True
    if args[0] == b'h':
        anguloTanque -= 1
        calculaAngulo = True
        

    if calculaAngulo:   
        lxTanque =   math.sin(anguloTanque*math.pi/180)
        lzTanque =   math.cos(anguloTanque*math.pi/180)
        # tanque_z = 0
        # if tanque_x > 0:
        #     tanque_x -= 1
    if args[0] == b'i':
        image.show()

    print('--------------')
    print(anguloTanque)
    print(lxTanque)
    print(lzTanque)
    print('--------------')
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


def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()
#**********************************************************************

def drawObj(obj:Objeto3d.Tri):
    obj.draw()

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

# glutMouseFunc(mouse)
# glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
