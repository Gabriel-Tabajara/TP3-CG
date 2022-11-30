import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
import numpy as np

class Objeto3d:
    pass

class Triangle:
    def __init__(self, a, b, c, normal):
        self.a = a
        self.b = b
        self.c = c
        self.normal = normal

class Tri2:
    def __init__(self, fileName) -> None:
        self.vertices = []
        self.indicies = []
        self.normal = None
        verticeDict = dict()
        verticesSet = set()
        a = 0
        pos = 0
        for line in open(fileName):
            print(a)
            a += 1
            line = line.split()
            if len(line) < 3: continue
            p1 = Ponto(float(line[0]), float(line[1]), float(line[2]))
            p2 = Ponto(float(line[3]), float(line[4]), float(line[5]))
            p3 = Ponto(float(line[6]), float(line[7]), float(line[8]))

            for p in [p1,p2,p3]:
                if p not in verticesSet: 
                    verticesSet.add(p)
                    verticeDict[p] = pos
                    self.vertices.append(p.x)
                    self.vertices.append(p.y)
                    self.vertices.append(p.z)
                    self.indicies.append(pos)
                    pos+=1
                else:
                    self.indicies.append(verticeDict[p])
        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.indicies = np.array(self.indicies, dtype=np.uint32)

        VBO = glGenBuffers(1, 10)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        


class Tri:
    def __init__(self, fileName) -> None:
        self.triangulos = []
        for line in open(fileName):
            line = line.split()
            if len(line) < 3: continue
            p1 = Ponto(float(line[0]), float(line[1]), float(line[2]))
            p2 = Ponto(float(line[3]), float(line[4]), float(line[5]))
            p3 = Ponto(float(line[6]), float(line[7]), float(line[8]))
            self.triangulos.append((Triangle(p1, p2, p3, self.prodVetUnitario(p1,p2,p3)), line[9]))

    def hex_to_rgb(value):
        value = value.lstrip('0x')

        cont = 0
        atual = ''
        rgb = []
        for letter in value: 
            atual += letter
            cont += 1
            if cont == 2:
                rgb.append(int(atual, 16))
                atual = ''
                cont = 0
        if cont != 0:
            rgb.append(int(atual, 16))
        return (rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    def prodVetUnitario(self, v1:Ponto,v2:Ponto,v3:Ponto):
        x = v1.y*v2.z - (v1.z * v2.y)
        y = v1.z*v2.x - (v1.x * v2.z)
        z = v1.x*v2.y - (v1.y * v2.x)
        vet = Ponto(x,y,z)
        modulo = math.sqrt(vet.x*vet.x + vet.y*vet.y + vet.z*vet.z)
        if modulo == 0: return vet
        else: return Ponto(x/modulo, y/modulo, z/modulo)
        # return Ponto(x,y,z)

    def draw(self):
        for tri in self.triangulos:
            triangulo: Triangle = tri[0]
            color = tri[1]
            glBegin(GL_TRIANGLES);
            try:
                r, g, b = Tri.hex_to_rgb(color)
                glColor3f(r, g, b)
            except:
                glColor3f(0,0,0)
            p1 = triangulo.a
            p2 = triangulo.b
            p3 = triangulo.c
            normal = triangulo.normal
            # normal = self.prodVetUnitario(p2-p1, p3-p2, p1-p3)
            glNormal3f(normal.x, normal.y, normal.z)
            # glScalef(0.5,0.5,0.5)
            glVertex3f(p1.x, p1.y, p1.z);
            glVertex3f(p2.x, p2.y, p2.z);
            glVertex3f(p3.x, p3.y, p3.z);
            # glScalef(2,2,2)
            glEnd();