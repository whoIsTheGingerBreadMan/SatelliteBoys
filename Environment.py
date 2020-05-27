from Satellite import Satellite
from Mass import TwoMassPoint
from collections import deque
import numpy as np
class World:

    def __init__(self,dt):
        self.satellites = {}
        self.masses = []
        self.dt = dt
        self.message_queue = deque()
        self.count = 0
        self.history = {}

    def add_satellite(self,name,x_init,v_init,clock_speed):
        if name in self.satellites:
            raise("NAME ERROR")
        else:
            print("ADDED SATELLITE " + str(name))
            self.satellites[name] = Satellite(name, x_init, v_init, self)
            self.add_to_history(name)

    def add_two_D_mass(self,M,x):
        self.masses.append(TwoMassPoint(M,x))


    def add_to_history(self,name):
        if name not in self.history:
            self.history[name] = {'x':[],'v':[],'t':[],'dists':[]}
        self.history[name]['x'].append(self.satellites[name].x)



    def step(self):
        self.count +=1
        #print("STEPPING STEP: " + str(self.count))
        for message in self.message_queue:
            print(message.dest)
            destinations = message.dest

            if len(destinations) == 0: # if target is all satellites or a single satellite
                if destinations ==0:  #broadcast
                    print(message.fs + ":BROADCAST")
                    for satellite_name in self.satellites:
                        satellite = self.satellites[satellite_name]
                        satellite._receive_message(message)
                else:
                    print(message.fs + " TRANSMIT TO " + message.dest)
                    self.satellites[destinations]._receive_message(message)

            else:   #target is multiple satellites but not a broadcast
                try:
                    for destination in destinations:
                        print(message.fs + " TRANSMIT TO " + destination)
                        self.satellites[destination]._receive_message(message)
                except:
                    raise("NAME ERROR")


        for satellite_name in self.satellites:

            satellite = self.satellites[satellite_name]
            #print("SATELLITE " + satellite.name + " PROPOGATING " )
            satellite._step()
            self.add_to_history(satellite_name)


def plot_history(world):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    fig = plt.figure()
    x_min= 10e10
    x_max = -10e10
    y_min = 10e10
    y_max = -10e10
    for mass in world.masses:
        plt.gca().add_patch(patches.Circle(mass.x,6371e3)) #EARTH
    for satellite in world.history:
        x = [x[0] for x in world.history[satellite]['x']]
        y = [x[1] for x in world.history[satellite]['x']]
        x_min = min(x_min,np.min(x))
        x_max = max(x_max,np.max(x))
        y_min = min(y_min, np.min(y))
        y_max = max(y_max, np.max(y))
        plt.scatter(x,y,s=1)
    print(x_min)
    print(x_max)
    print(y_min)
    print(y_max)
    #plt.gca().set_xlim(x_min,x_max)
    #plt.gca().set_ylim(y_min, y_max)
    plt.show()

if __name__ == "__main__":
    world = World(10)
    world.add_two_D_mass(5.97e24,[0,0])
    for i in range(1):
        x_init = np.array([0,6800e3]) + np.random.random(2)*100
        v_init = np.array([10,0])#np.random.random(2)*1000
        cs = 200
        world.add_satellite(i,x_init,v_init,cs)
    for _ in range(100000):
        world.step()
    plot_history(world)







