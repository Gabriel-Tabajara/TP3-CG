import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto

class Triangle:
    def __init__(self, a, b, c, normal):
        self.a = a
        self.b = b
        self.c = c
        self.normal = normal


class Tri:
    def __init__(self, fileName) -> None:
        self.minX = 100000000
        self.maxX = -100000000
        self.minY = 100000000
        self.maxY = -100000000
        self.minZ = 100000000
        self.maxZ = -100000000
        self.triangulos = []
        for line in open(fileName):
            line = line.split()
            if len(line) < 3: continue
            p1 = Ponto(float(line[0]), float(line[1]), float(line[2]))
            p2 = Ponto(float(line[3]), float(line[4]), float(line[5]))
            p3 = Ponto(float(line[6]), float(line[7]), float(line[8]))
            self.minX = min(self.minX, p1.x, p2.x, p3.x)
            self.minY = min(self.minY, p1.y, p2.y, p3.y)
            self.minZ = min(self.minZ, p1.z, p2.z, p3.z)
            self.maxX = max(self.maxX, p1.x, p2.x, p3.x)
            self.maxY = max(self.maxY, p1.y, p2.y, p3.y)
            self.maxZ = max(self.maxZ, p1.z, p2.z, p3.z)
            try:
                self.triangulos.append((Triangle(p1, p2, p3, self.prodVetUnitario(p1,p2,p3)), line[9]))
            except:
                self.triangulos.append((Triangle(p1, p2, p3, self.prodVetUnitario(p1,p2,p3)), None))

    
    def colision(self, x, y, z):
        # use minX, maxX, minY, maxY, minZ, maxZ to check colision
        if x < self.minX or x > self.maxX: return False
        if y < self.minY or y > self.maxY: return False
        if z < self.minZ or z > self.maxZ: return False
        return True

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
            glBegin(GL_TRIANGLES);
            try:
                color = tri[1]
                r, g, b = Tri.hex_to_rgb(color)
                glColor3f(r, g, b)
            except:
                glColor3f(0,0,0)
            p1 = triangulo.a
            p2 = triangulo.b
            p3 = triangulo.c
            normal = triangulo.normal
            glNormal3f(normal.x, normal.y, normal.z)
            glVertex3f(p1.x, p1.y, p1.z);
            glVertex3f(p2.x, p2.y, p2.z);
            glVertex3f(p3.x, p3.y, p3.z);
            glEnd();


