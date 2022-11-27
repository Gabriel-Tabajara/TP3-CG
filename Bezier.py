
from Ponto import Ponto
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Bezier:
    def __init__NEW(self, p0:Ponto, p1:Ponto, p2:Ponto):
        print ("Construtora da Bezier")
        self.ComprimentoTotalDaCurva = 0.0
        self.Coords = []
        self.Coords += [p0]
        self.Coords += [p1]
        self.Coords += [p2]
        #P = self.Coords[0]
        #P.imprime()

    def __init__(self, *args:Ponto, pid=0):
        #print ("Construtora da Bezier")
        self.ComprimentoTotalDaCurva = 0.0
        self.Coords = []
        self.id = pid
        self.p1 = args[0]
        self.p2 = args[1]
        self.p3 = args[2]
        #print (args)
        for i in args:
            self.Coords.append(i)
        #P = self.Coords[2]
        #P.imprime()

    def __str__(self):
        return f'Bezier {self.id} ({self.p1}) ({self.p3})'

    def Calcula(self, t) -> Ponto:
        P = Ponto()
        P = self.Coords[0] * (1-t) * (1-t) + self.Coords[1] * 2 * (1-t) * t + self.Coords[2] * t*t
        return P

    def Traca(self, color=None):     
        # if color: glColor3ub(color[0], color[1], color[2])
        
        t=0.0
        DeltaT = 1.0/50
        P:Ponto = Ponto
        glBegin(GL_LINE_STRIP)
        glColor3f(0,0,1)
        
        while(t<1.0):
            P = self.Calcula(t)
            glVertex3f(P.x, P.y, P.z)
            t += DeltaT
        P = self.Calcula(1.0) #faz o acabamento da curva
        glVertex3f(P.x, P.y, P.z)
        
        glEnd()

           
            