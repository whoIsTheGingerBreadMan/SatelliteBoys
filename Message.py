

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
    def __init__(self,time_stamp,cs,from_sat, send_to=0,amplitude=0):
        self.ts=time_stamp
        self.cs = cs
        self.fs = from_sat
        self.dest = send_to




