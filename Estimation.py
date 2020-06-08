import numpy as np
from scipy.spatial import distance_matrix
import Satellite


class Filter:
    """
    The filters to estimate satellite distance and mass density distribution

    """
    def __init__(self):
        super().__init__()
        self.x_est = 0
        self.v_est = 0
        self.satellite_num = 4
        # particle number
        self.N = 200
        
    def EKF_filter(self):
        pass

    def particle_filter(self, dt, D_matrix, Q, R, N):
        x_prev = np.zeros((satellite_num * 4, N))
        # predict
        u = np.zeros((satellite_num * 4, N)) # Assumption: dt is small enough that the acceleration can be ignored
        noise_w = Q * np.random.randn(satellite_num * 4, N)
        x_new = transition_dyn(dt, u, x_prev) + noise_w

        # update
        w = np.zeros(N)
        for i in range(N):
            # for j in range(self.satellite_num):
            #     x_array = 
            coordinates = x_new[:2*self.satellite_num, i]
            D_gen = distance_matrix(coordinates, coordinates)
            w[i] = 1/np.sqrt((2*np.pi)**self.satellite_num * np.linalg.det(R)) * np.exp(-1/2* (D_matrix - D_gen).T.dot(np.linalg.inv(R)).dot(D_matrix - D_gen))
        w = w / np.sum(w)

        # resample
        for i in range(N):
            for j in range(4 * self.satellite_num):
                x_prev[j, i] = np.random.choice(population=x_new[j, :], weights=w)


    def transition_dyn(self, dt=None, u=0, x_prev=0):
        # for mass in self.env.masses:
            # u += mass.get_acceleration(x_est)
        x_est = x_prev[:self.satellite_num*2, :]
        v_est = x_prev[self.satellite_num*2:, :]
        if dt != None:
            x_est += .5*u*dt**2 + v_est * dt
            v_est += u * dt
        elif self.env!=None:
            dt = self.env.dt
            x_est += .5*u*dt**2 + v_est * dt
            v_est += u * dt
        else:
            raise("No dt or environment.")

        x_new = np.concatenate(x_est, v_est)

        return x_new