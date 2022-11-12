from GeomBase import *
from SliceAlgo import *
from StlModel import *


def writeAptFile(layers,pathIn, pathOut):
    # 计算法向量，起点，终点，
    t = 0.1
    N = readStlNormal(pathIn)
    Fp1 = layers.startPoint()
    Fp = Fp1 + N.amplified(t)
    Ep1 = layers.endPoint()
    Ep = Ep1 + N.amplified(t)

    f = None
    try:
        f = open(pathOut, 'w+')
        f.write("PARTNO/123\n")
        f.write("RAPID\n"+'GOTO/%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (Fp.x, Fp.y, Fp.z,N.dx,N.dy,N.dz))
        #for layer in layers:
            #for pt in layer.contours[0].points:
                #f.write("GOTO/"+'%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (pt.x, pt.y, pt.z,N.dx,N.dy,N.dz))
        for pt in layers.points:
            f.write("GOTO/" + '%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (pt.x, pt.y, pt.z, N.dx, N.dy, N.dz))
        f.write("RAPID\n" + 'GOTO/%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (Ep.x, Ep.y, Ep.z,N.dx,N.dy,N.dz))
        f.write("END")
    except Exception as ex:
        print(ex)
    finally:
        if f:
            f.close()

def getCoords(line):
    strs = line.lstrip().split(' ')
    cnt = len(strs)
    return float(strs[cnt-3]), float(strs[cnt-2]), float(strs[cnt-1])

#读第一个面片法向
def readStlNormal(filepath):
    f = None
    try:
        f = open(filepath, 'r')
        while True:
            line = f.readline().strip('\n')
            if line is None or line == '':
                break
            if 'facet normal' in line:
                dx, dy, dz = getCoords(line)
                n = Vector3D(dx, dy, dz)
                break
        return n
    except Exception as ex:
        print(ex)
    finally:
        if f:
            f.close()

#每层进行连接
def linklayers(layers):
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


def GenPath(pathIn,layerThk):
    '''va = VtkAdaptor()
    src = vtk.vtkSTLReader()
    src.SetFileName(pathIn)
    va.drawPdSrc(src).GetProperty().SetOpacity(0.5)'''

    stlModel = StlModel()
    stlModel.readStlFile(pathIn)                  #直接读文本格式的STL
    #layers = slice_topo(stlModel, 5)
    layers = intersectStl_sweep(stlModel, layerThk)
    for layer in layers:
        layer.contours = linkSegs_brutal(layer.segments)
        layer.segments.clear()
        adjustPolygonDirs(layer.contours)         #判断方向-改!!!
    layers = linklayers(layers)

    '''for layer in layers:
        for contour in layer.contours:
            va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
    va.display()'''

    Poly = LayersToPolyline(layers)
    return Poly


if __name__=='__main__':
    Layers=GenPath("E:\\2D polygon2.stl", 5)
    writeAptFile(Layers, "E:\\2D polygon2.stl", "E:\\3.Apt")