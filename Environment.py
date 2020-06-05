from Satellite import Satellite
from Mass import TwoMassPoint
from collections import deque
import numpy as np
import Constants
import Plots

debug = Constants.debug
show_steps = Constants.show_steps
keep_history = Constants.keep_history

class World:

    def __init__(self,dt,synchronous:bool=True):
        self.time = 0
        self.satellites = {}
        self.masses = []
        self.dt = dt
        self.message_queue = deque()
        self.count = 0
        self.history = {}
        self._synchronous = synchronous #Do not edit me

    def add_satellite(self,name,x_init,v_init,clock_speed,emit_rate):
        if name in self.satellites:
            raise("NAME ERROR")
        else:
            if debug:
                print("ADDED SATELLITE " + str(name))
            self.satellites[name] = Satellite(name, x_init, v_init,self,clock_speed,emit_rate)
            self.add_to_history(name)

    def add_two_D_mass(self,M,x):
        self.masses.append(TwoMassPoint(M,x))


    def add_to_history(self,name):
        if name not in self.history:
            self.history[name] = {'x':[],'v':[],'t':[],'dists':[]}
        self.history[name]['x'].append(self.satellites[name].x)
        self.history[name]['v'].append(self.satellites[name].v)



    def step(self):
        self.count +=1
        self.time += self.dt
        #print("STEPPING STEP: " + str(self.count))
        while(self.message_queue):
            message = self.message_queue.popleft()

            if debug:
                print(message.dest)
            destinations = message.dest

            if type(destinations) == int: # if target is all satellites or a single satellite
                if destinations ==0:  #broadcast
                    if debug:
                        print(message.from_sat + ":BROADCAST")
                    for satellite_name in self.satellites:
                        if str(message.from_sat)!=str(satellite_name):
                            satellite = self.satellites[satellite_name]
                            if self._synchronous:
                                arrival_time = message.calculate_arrival_time(satellite.x)
                                satellite._receive_message(message,arrival_time)
                            else:
                                satellite._receive_message(message)
                else:
                    if debug:
                        print(message.from_sat + " TRANSMIT TO " + message.dest)
                    self.satellites[destinations]._receive_message(message)

            elif(type(destinations)==list):   #target is multiple satellites but not a broadcast
                try:
                    for destination in destinations:
                        if debug:
                            print(message.from_sat + " TRANSMIT TO " + destination)
                        self.satellites[destination]._receive_message(message)
                except:
                    raise("NAME ERROR")


        for satellite_name in self.satellites:

            satellite = self.satellites[satellite_name]
            #print("SATELLITE " + satellite.name + " PROPOGATING " )
            satellite._step()
            self.add_to_history(satellite_name)





if __name__ == "__main__":
    world = World(.01,synchronous=True)
    world.add_two_D_mass(1e24,[0,-8371e3])
    for i in range(5):
        x_init = np.array([0,0]) + np.random.randn(2)*10
        v_init = np.array([500,0])+np.random.randn(2)*10
        clock_speed = .01  #in 1/frequency
        emit_rate=100
        world.add_satellite(i,x_init,v_init,clock_speed,emit_rate)
    for i in range(5000):
        if(show_steps):
            print(i)
        world.step()
    Plots.plot_satellite_distances(world,0)
    Plots.plot_history(world)







