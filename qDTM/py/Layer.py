class Layer:
    def __init__(self, z):
        self.z = z
        self.segments = []
        self.contours = []
        #最后一章需要
        self.shellContours = []
        self.ffContours = []
        self.sfContours = []
