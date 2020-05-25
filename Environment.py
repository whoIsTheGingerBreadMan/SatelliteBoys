from Satellite import Satellite
class World:

    def __init__(self,dt):
        self.satellites = []
        self.dt = dt

    def add_satellite(self,name,x_init,v_init,clock_speed):
        sat = Satellite(name,x_init,v_init,self)
        self.satellites.append(sat)

    def step(self):
        for satellite in self.satellites:
            satellite._step()



