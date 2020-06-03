
import numpy as np
from scipy.spatial import distance
import Constants
debug = Constants.debug
keep_history = Constants.keep_history

class Message:
    """
    The message of a satellite.
    time_stamp is the sending satellites local time stamp
    cs is the clock speed of the sending satellite
    from_sat is the sender satellite id.
    send_to is the target satellites.
    send_to = 0 means global transmission
    send_to = [1,2,3] means attempt to transmit to satellites 1,2,3
    send_to = 1 means attempt to transmit to satellites 1
    amplitude represents the strength of the signal. For now it's irrelevant.
    from
    """
    def __init__(self,time_stamp,cs,from_sat,start_location, send_to=0,amplitude=0):
        self.time_stamp=time_stamp
        self.clock_speed = cs
        self.from_sat = from_sat
        self.dest = send_to
        self.start_location = start_location
    def calculate_arrival_time(self,location):
        location_diff = distance.euclidean(self.start_location,location)
        return (location_diff/Constants.C) + self.time_stamp









