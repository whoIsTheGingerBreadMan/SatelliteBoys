import numpy as np
import threading
import logging
from scipy.spatial import distance
import time
from Message import Message
from collections import deque
import Constants

debug = Constants.debug
show_steps = Constants.show_steps
keep_history = Constants.keep_history

def print_location_and_velocity(name,x,v):
    print("SATELLITE " + str(name) + " STARTING LOCATION: " + x.__str__() + " STARTING "
                                                                                 "VELOCITY: "
          + v.__str__())

class Satellite:
    def __init__(self,name,x_init,v_init,env=None,clock_speed:float=.1,emit_rate:int=10):
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
        self.clock_speed = clock_speed   #The clock speed in number of clock cycles per second
        self.count = 0
        self.env = env
        self.T = 0
        self.prev_T = 0
        # self.num_steps_to_signal = 10
        self.satellite_distances = {}
        self.message_buffer = []
        self.emit_rate = emit_rate
        self.satellite_distances_hist = {}

    def _step(self,dt=None,u=0):  #move in time. Do m
        if debug:
            print(self.name + ": ")
        for mass in self.env.masses:
            u += mass.get_acceleration(self.x)
        if dt != None:
            self.x = .5*u*dt**2 +self.v* dt + self.x
            self.v = u * dt + self.v
        elif self.env!=None:
            dt = self.env.dt
            self.x = .5*u*dt**2 +self.v*self.env.dt + self.x
            self.v = u*dt+self.v
            if debug:
                print_location_and_velocity(self.name, self.x, self.v)
        else:
            raise("No dt or environment.")

        self.T += dt
        if(self.T-self.prev_T>=self.clock_speed):
            #print("CLOCK TICK: " + self.name )
            num_clock_cycles = (self.T-self.prev_T)//self.clock_speed
            self.count += num_clock_cycles
            self.prev_T += self.clock_speed*num_clock_cycles
            if(self.count%self.emit_rate==0):
                self.transmit_message()
            self.update_locations()

    def calculate_distance(self,message:Message,accept_time:float=0):
        if not accept_time:
            sat_sent_time = message.time_stamp*message.clock_speed
            sat_rec_time = self.get_satellite_time()
            dt = abs(sat_sent_time - sat_rec_time)
        else:
            sat_sent_time = message.time_stamp
            sat_rec_time = (accept_time//self.clock_speed)*self.clock_speed
            dt = abs(sat_sent_time - sat_rec_time)
        return dt*Constants.C

    def transmit_message(self):

        message = Message(self.count*self.clock_speed,self.clock_speed,self.name,self.x)
        self.env.message_queue.append(message)


    def _receive_message(self, m:Message,accept_time:float):
        if show_steps:
            pass
            #print("Receiving Message: " +self.name + " From: " + m.from_sat)
        self.message_buffer.append((m,accept_time))

    def update_locations(self):
        #print("Updating locations")
        while(self.message_buffer):
            m,accept_time = self.message_buffer.pop()
            if m.from_sat not in self.satellite_distances:
                if(debug):
                    print("New satellite: " + m.from_sat)
                self.satellite_distances[str(m.from_sat)] = 0
            self.satellite_distances[str(m.from_sat)] = (self.calculate_distance(m,accept_time),
                                                    self.count)
            if keep_history:
                if m.from_sat not in self.satellite_distances_hist:
                    self.satellite_distances_hist[str(m.from_sat)] = []
                distance = self.calculate_distance(m,accept_time)
                self.satellite_distances_hist[str(m.from_sat)].append((distance,accept_time))



                #print(self.name)

    def get_satellite_time(self):
        return self.clock_speed*self.count

    def _send_signal(self,dest=0):
        time = self.get_satellite_time()
        msg = self.name + " is sending a message to " + dest + " at time " + time
        self.env.message_queue.append(Message(time,self.name,dest))













