from GeomBase import *


class Triangle:
    def __init__(self, A, B, C, N = Vector3D(0, 0, 0)):
        self.A, self.B, self.C, self.N = A.clone(), B.clone(), C.clone(), N.clone()
        self.zs = []

    def __str__(self):
        pass

    def zMinPnt(self):
        if self.A.z < self.B.z and self.A.z < self.C.z:
            return self.A
        elif self.B.z < self.A.z and self.B.z < self.C.z:
            return self.B
        else:
            return self.C

    def zMaxPnt(self):
        if self.A.z > self.B.z and self.A.z > self.C.z:
            return self.A
        elif self.B.z > self.A.z and self.B.z > self.C.z:
            return self.B
        else:
            return self.C

    def lengthSquare(self):
        return self.N.dx * self.N.dx + self.N.dy * self.N.dy + self.N.dz * self.N.dz

    def length(self):
        return math.sqrt(self.lengthSquare())

    def calcNormal(self):
        len = self.length()
        self.N.dx, self.N.dy, self.N.dz = self.N.dx / len, self.N.dy / len, self.N.dz / len

