import math
#placeholder quaternion

class Quaternion(object):
    def __init__(self, w=0, x=0, y=0 ,z=1):
        self._w = float(w)
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)
    
    def set(self, w, x, y, z):
        self._w = float(w)
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)