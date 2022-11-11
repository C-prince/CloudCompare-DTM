from GeomBase import *
from SliceAlgo import *
from VtkAdaptor import *
from StlModel import *


def writeAptFile(polys,pathIn, pathOut):
    t = 0.1
    N = readStlNormal(pathIn)
    Fp1 = polys.startPoint()
    Fp = Fp1 + N.amplified(t)
    Ep1 = polys.endPoint()
    Ep = Ep1 + N.amplified(t)

    f = None
    try:
        f = open(pathOut, 'w+')
        f.write("PARTNO/123\n")
        f.write("RAPID\n"+'GOTO/%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (Fp.x, Fp.y, Fp.z,N.dx,N.dy,N.dz))
        for pt in polys.points:
            f.write("GOTO/"+'%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n' % (pt.x, pt.y, pt.z,N.dx,N.dy,N.dz))
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


def GenPath(pathIn,layerThk):
    va = VtkAdaptor()
    src = vtk.vtkSTLReader()
    src.SetFileName(pathIn)
    va.drawPdSrc(src).GetProperty().SetOpacity(0.5)

    stlModel = StlModel()
    stlModel.extractFromVtkStlReader(src)
    layers = intersectStl_sweep(stlModel, layerThk)
    for layer in layers:
        layer.contours = linkSegs_brutal(layer.segments)
        layer.segments.clear()  
        adjustPolygonDirs(layer.contours)         #判断方向-改!!!
    layers = linklayers(layers)

    for layer in layers:
        for contour in layer.contours:
            va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
    #va.drawPoint(Fp)
    #va.drawPoint(Ep)
    va.display()
    
    Poly = LayersToPolyline(layers)
    return Poly


if __name__=='__main__':
    Polys=GenPath("E:\\2D polygon2.stl", 5)
    writeAptFile(Polys, "E:\\2D polygon2.stl", "E:\\2.Apt")
