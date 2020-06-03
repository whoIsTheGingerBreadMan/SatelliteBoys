import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
def plot_history(world):
    #fig = plt.figure()
    x_min= 10e10
    x_max = -10e10
    y_min = 10e10
    y_max = -10e10
    names = []
    plots = []
    for mass in world.masses:
        plt.gca().add_patch(patches.Circle(mass.x,6371e3)) #EARTH
    for satellite in world.history:
        x = [x[0] for x in world.history[satellite]['x']]
        y = [x[1] for x in world.history[satellite]['x']]
        u =  [x[0] for x in  world.history[satellite]['v'][::1000]]
        v = [x[1] for x in world.history[satellite]['v'][::1000]]

        x_min = min(x_min,np.min(x))
        x_max = max(x_max,np.max(x))
        y_min = min(y_min, np.min(y))
        y_max = max(y_max, np.max(y))
        plots.append(plt.scatter(x,y,s=1))
        plt.quiver(x[::1000],y[::1000],u,v)
        names.append(satellite)

    plt.gca().set_xlim(x_min,x_max)
    plt.gca().set_ylim(y_min, y_max)
    plt.gca().set_aspect('equal')
    plt.legend(plots,names)

    plt.show()

def plot_satellite_distances(world,from_sat:int = 0):
    import matplotlib.pyplot as plt
    import sys
    MAX = -sys.maxsize
    MIN = sys.maxsize
    plots = []
    names = []
    for to_sat in world.satellites:
        if not int(to_sat) == int(from_sat):
            distances_for_sat = world.satellites[int(from_sat)].satellite_distances_hist[str(to_sat)]
            distances = [x[0] for x in distances_for_sat]
            _max = max(distances)
            _min = min(distances)
            plt.plot(distances,label=to_sat)
            if _max>MAX:
                MAX = _max
            if _min<MIN:
                MIN = _min

    plt.legend()
    plt.gca().set_ylim(MIN-10,MAX+10)

    plt.show()