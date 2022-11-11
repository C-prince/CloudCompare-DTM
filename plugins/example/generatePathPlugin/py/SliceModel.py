import SliceAlgo
from VtkAdaptor import *
from StlModel import *


class SliceModel:
    def __init__(self, stlModel, layerThk, sliceAlgo="brutal"):
        self.stlModel = stlModel
        self.layerThk = layerThk
        if sliceAlgo == 'brutal':
            self.slice_brutal()
        elif sliceAlgo == 'optimal':
            self.slice_optimal()

    def slice_brutal(self):
        self.layers = SliceAlgo.intersectStl_brutal(self.stlModel, self.layerThk)
        for layer in self.layers:
            layer.contours = SliceAlgo.linkSegs_brutal(layer.segments)
            SliceAlgo.adjustPolygonDirs(layer.contours)

    def slice_optimal(self):
        self.layers = SliceAlgo.intersectStl_sweep(self.stlModel, self.layerThk)
        for layer in self.layers:
            layer.contours = SliceAlgo.linkSegs_dlook(layer.segments)
            layer.segments.clear()  # 修正轮廓方向
            SliceAlgo.adjustPolygonDirs(layer.contours)

    def writeSlcFile(self, path):
        SliceAlgo.writeSlcFile(self.layers, path)

    def readSlcFile(self, path):
        self.layers = SliceAlgo.readSlcFile(path)

    def drawLayerContours(self, va, start=0, stop=0xFFFF, step=1, clr=(0, 0, 0), lineWidth=1):
        for i in range(max(0, start), min(stop, len(self.layers)), step):
            layer = self.layers[i]
            for contour in layer.contours:
                contourActor = va.drawPolyline(contour)
                contourActor.GetProperty().SetColor(clr)
                contourActor.GetProperty().SetLineWidth(lineWidth)

#组合优化切片连接行得通
if __name__ == '__main__':
    va = VtkAdaptor()
    stlModel = StlModel()

    '''stlModel.readStlFile("E:\\m1.stl")'''#stlmodel类没有显示模型功能

    vtkStlReader = vtk.vtkSTLReader()
    vtkStlReader.SetFileName("E:\\2D polygon.stl")
    va.drawPdSrc(vtkStlReader).GetProperty().SetOpacity(0.5)#显示模型
    stlModel.extractFromVtkStlReader(vtkStlReader)

    sliceModel = SliceModel(stlModel, 0.03, 'optimal')
    sliceModel.drawLayerContours(va)
    va.display()
