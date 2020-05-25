import numpy as np
import threading
import logging
from scipy.spatial import distance
import time

class Satellite:
    def __init__(self,name,x_init,v_init,env=None):
        self.name = name
        self.x = x_init
        self.v = v_init
        self.fs = 100
        self.count = 0
        self.env = env
        self.T = 0
        self.prev_T = 0
        self.num_steps_to_signal = 10

    def _step(self,dt=None,u=0):
        if dt != None:
            self.x = .5*u*dt**2 +self.v* dt + self.x
        elif self.env!=None:
            dt = self.env.dt
            self.x = .5*u*dt**2 +self.v*dt + self.x
        else:
            raise("No dt or environment.")

        self.T += dt
        if(self.T-self.prev_T>=self.fs):
            num_clock_cycles = (self.T-self.prev_T)//self.fs
            self.count += num_clock_cycles
            self.prev_T += self.fs*num_clock_cycles

    def broadcast(self): #probably better to do this asynchronously but I'm too dumb.
        for sat in self.env.satellites:
            self._send_signal(sat.name)


    def get_satellite_time(self):
        return self.fs*self.count

    def _send_signal(self,dest):
        time = self.get_satellite_time()
        msg = self.name + " is sending a message to " + dest + " at time " + time
        logging.debug(msg)
        T = self.env.get_time_of_flight(dest,self)
        time.sleep(T) ## Waiting the amount of time it would take for the signal to reach targe


    def _recieve_signal(self):

        return


# def run_satellite(name,x_init,v_init,clock_speed,env):
#     world_lock = threading.
#     sat = Satellite(name,x_init,v_init,clock_speed,env)
#     lock = threading.Lock()
#
#     while True:
#
#         sat.step()








