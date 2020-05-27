import numpy as np
import threading
import logging
from scipy.spatial import distance
import time
from Message import Message
from collections import deque


def print_location_and_velocity(name,x,v):
    print("SATELLITE " + str(name) + " STARTING LOCATION: " + x.__str__() + " STARTING "
                                                                                 "VELOCITY: "
          + v.__str__())

C = 3000  #message propogation speed (speed of light)
class Satellite:
    def __init__(self,name,x_init,v_init,env=None):
        """
        A single satellite which has a name an inital position, an initial velocity,
        and an environment... Possibly let's add a range and possible modulation with distance.
        For now we will only haven environment and no threading. See the drawing.
        https://docs.google.com/drawings/d/1FD8a_BdKKHfmQgiWNVbbFE7OiL1AgCTqUrTZn_unoL8/edit?usp=sharing
        :param name:
        :param x_init:
        :param v_init:
        :param env:
        """
        self.name = str(name)
        self.x = x_init
        self.v = v_init
        #print_location_and_velocity(self.name, self.x, self.v)
        self.cs = 1/100   #The clock speed in number of clock cycles per second
        self.count = 0
        self.env = env
        self.T = 0
        self.prev_T = 0
        self.num_steps_to_signal = 10
        self.satellite_distances = {}
        self.message_buffer = []

    def _step(self,dt=None,u=0):  #move in time. Do m
        #print(self.name + ": ")
        for mass in self.env.masses:
            u += mass.get_acceleration(self.x)
        if dt != None:
            self.x = .5*u*dt**2 +self.v* dt + self.x
            self.v = u * dt + self.v
        elif self.env!=None:
            dt = self.env.dt
            self.x = .5*u*dt**2 +self.v*self.env.dt + self.x
            self.v = u*dt+self.v
            #print_location_and_velocity(self.name, self.x, self.v)
        else:
            raise("No dt or environment.")

        self.T += dt
        if(self.T-self.prev_T>=self.cs):
            #print("CLOCK TICK: " + self.name )
            num_clock_cycles = (self.T-self.prev_T)//self.cs
            self.count += num_clock_cycles
            self.prev_T += self.cs*num_clock_cycles
            self.transmit_message()
            self.update_locations()

    def calculate_distance(self,message):
        dt = abs(message.ts*message.cs - self.get_satellite_time())
        return dt*C

    def transmit_message(self):
        return
        message = Message(self.count,self.cs,self.name)
        self.env.message_queue.append(message)


    def _receive_message(self, m):
        self.message_buffer.append(m)

    def update_locations(self):
        #print("Updating locations")
        while(self.message_buffer):
            m = self.message_buffer.pop()
            if m.fs not in self.satellite_distances:
                print("New satellite: " + m.fs)
                self.satellite_distances[str(m.fs)] = 0
            self.satellite_distances = (self.calculate_distance(m),self.count)
            #print(self.name)

    def get_satellite_time(self):
        return self.cs*self.count

    def _send_signal(self,dest=0):
        time = self.get_satellite_time()
        msg = self.name + " is sending a message to " + dest + " at time " + time
        logging.debug(msg)
        self.env.message_queue.append(Message(time,self.name,dest))













