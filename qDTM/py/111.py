from Polyline import *
from SliceAlgo import *


def getCoords(line):
    strs = line.lstrip().split(' ')
    return float(strs[0]), float(strs[1]), float(strs[2])


seg9 = Polyline()

#读txt坐标点并储存为Point3D
f = None
try:
    f = open("E:\\Contour.txt", 'r')
    while True:
        line = f.readline().strip('\n')
        if line is None or line == '':
            break
        dx, dy, dz = getCoords(line)
        A = Point3D(dx, dy, dz)
        seg9.addPoint(A)
except Exception as ex:
    print(ex)
finally:
    if f:
        f.close()
seg9.addPoint(seg9.startPoint())


va = VtkAdaptor()
va.drawPolyline(seg9).GetProperty().SetColor(0, 0, 0)
va.display()
