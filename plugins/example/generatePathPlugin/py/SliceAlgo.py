from VtkAdaptor import *
from StlModel import *
from GeomBase import *
from Layer import *
from GeomAlgo import *
from IntersectStl_sweep import *
import struct
from Polyline import *




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
            #if contour.isClosed():
                #break
    return contours


def intersectStl_sweep(stlModel, layerThk):                             #优化截交：扫描平面法
    return IntersectStl_sweep(stlModel, layerThk).layers


def linklayers(layers):        #每层进行连接
    q = len(layers) // 2
    for i in range(q):
        d = i * 2
        endp = layers[d].contours[0].endPoint()
        layers[d + 1].contours[0].addPoint(endp)
        layers[d + 1].contours[0].reverse()
        firstp = layers[d + 1].contours[0].endPoint()
        if (d + 2) < len(layers):
            layers[d + 2].contours[0].raddPoint(firstp)
        else:
            break
    return layers


def LayersToPolyline(layers):
    poly=Polyline()
    for layer in layers:
        for pt in layer.contours[0].points:
            poly.addPoint(pt.clone())
    return poly