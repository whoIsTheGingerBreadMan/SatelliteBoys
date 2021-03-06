import numpy as np
from scipy.spatial import distance
G = 6.67e-11 # Gravitational Constant

class TwoMassPoint:
    def __init__(self,M,x):
        self.GM = G*M
        self.x = np.array(x)
    def get_acceleration(self,x2):
        vector = -1*(np.array(x2)-self.x)
        D = distance.euclidean(x2,self.x)
        uv = vector/D
        acceleration = uv*self.GM/(D**2)
        return acceleration




