#from VtkAdaptor import *
from StlModel import *
from GeomBase import *
from Layer import *
from GeomAlgo import *
from IntersectStl_sweep import *
import struct


def intersectStl_brutal(stlModel, layerThk):                             #直接截交：暴力法(×)
    layers = []
    xMin, xMax, yMin, yMax, zMin, zMax = stlModel.getBounds()
    z = zMin + layerThk
    while z < zMax:
        layer = Layer(z)
        for tri in stlModel.triangles:
            seg = intersectTriangleZPlane(tri, z)
            if seg is not None:
                layer.segments.append(seg)
        layers.append(layer)
        z += layerThk
    return layers


def linkSegs_brutal(segs):                                              #截交线段拼接：暴力法(×)
    segs = list(segs)
    contours = []
    while len(segs) > 0:
        contour = Polyline()
        contours.append(contour)
        while len(segs) > 0:
            for seg in segs:
                if contour.appendSegment(seg):
                    segs.remove(seg)
                    break
            if contour.isClosed():
                break
    return contours


def intersectStl_sweep(stlModel, layerThk):                             #优化截交：扫描平面法
    return IntersectStl_sweep(stlModel, layerThk).layers





def writeSlcFile(layers, path):
    f = None
    try:
        f = open(path, 'w+b')
        f.write(bytes("-SLCVER 2.0 -UNIT MM", encoding='utf -8'))
        f.write(bytes([0x0d, 0x0a, 0x1a]))
        f.write(bytes([0x00]*256))
        f.write(struct.pack('b', 1))
        f.write(struct.pack('4f', 0, 0, 0, 0))
        for layer in layers:
            f.write(struct.pack('fI', layer.z, len(layer.contours)))
            for contour in layer.contours:
                f.write(struct.pack('2I', contour.count(), 0))
                for pt in contour.points:
                    f.write(struct.pack('2f', pt.x, pt.y))
        f.write(struct.pack('fI', layers[-1].z, 0xFFFFFFFF))
    except Exception as ex:
        print(" writeSlcFile exception :", ex)
    finally:
        if f:
            f.close()


def readSlcFile(path):
    f, layers, i = None, [], 0
    try:
        f = open(path, 'rb')
        data = f.read()
        while True:
            if data[i] == 0x0d and data[i+1] == 0x0a and data[i+2] == 0x1a:
                break
            i += 1
        i += (3+256)
        channelCount = data[i]
        i += (1 + channelCount * 16)
        while True:
            z, = struct.unpack('f', data[i: i + 4])
            i += 4
            contourCount, = struct.unpack('I', data[i: i + 4])
            i += 4
            if contourCount == 0xFFFFFFFF:
                break
            layer = Layer(z)
            for j in range(contourCount):
                pointCount, = struct.unpack('I', data[i: i + 4])
                i += 4
                gapCount, = struct.unpack('I', data[i: i + 4])
                i += 4
                contour = Polyline()
                for k in range(pointCount):
                    x, y = struct.unpack('2f', data[i: i + 8])
                    i += 8
                    contour.addPoint(Point3D(x, y, z))
                layer.contours.append(contour)
            layers.append(layer)
    except Exception as ex:
        print(" readSlcFile exception :", ex)
    finally:
        if f:
            f.close()
        return layers
