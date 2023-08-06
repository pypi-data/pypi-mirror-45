#spec = [('data',float64[:]),
#       ('theta0', float64[:]),
#       ('C',int32[:]),
#       ('B',int32[:])]
#
#@jitclass(spec)
#@numba.vectorize()#
#def grad_u(data, theta, n, f):
#    batch = data[np.random.randint(data.shape[0], size=n), :]
#    s = 0
#    for x in batch:
#        s += f(x, theta)
#    return -s / n

#@jit
#def traj(length, f, theta0, r0, epsilon, size):
#    for i in range(length):
#        theta_m, r_m = f(theta0,r0,epsilon,size)
#        theta0, r0 = theta_m, r_m
#    return theta0
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import numba
from functools import partial
import multiprocessing
import random
from scipy import stats
@numba.guvectorize([(numba.float64[:,:], numba.float64[:], numba.float64[:])], '(m,n),(n)->(m)',target='parallel')
def vel(A, B, v):
    m,n = A.shape
    v = np.zeros(m)
    for i in range(m):
        for j in range(n):
            v[i] += A[i,j]*B[j]
    
class sghmc_jit():
    def __init__(self,lnp,lnp_grad,initialguess,C,data = None, usedata = False,B=None,M=None,logpri=None):
        '''
        
        '''
        self.data = data 
        self.ndim = len(initialguess)
        self.get_mass_matrix(M)
        self.theta0 = initialguess
        self.lnp = lnp
        self.lnp_grad = lnp_grad
        self.res = []
        self.C = C
        self.usedata = usedata 
        if usedata:
            self.n = len(data)
        if B is None:
            self.B = np.zeros_like(C)
        else:
            self.B = B
            
        
    def get_mass_matrix(self, mass_matrix=None):
        """
        get the inverse of the mass matrix
        """
        if mass_matrix is None:
            self.mass_matrix = np.identity(self.ndim)
            self.inverse_mass_matrix = np.identity(self.ndim)
        else:
            if len(mass_matrix) != self.ndim:
                print("Invalid mass matrix")
            elif len(mass_matrix) == 1:
                self.mass_matrix = mass_matrix
                self.inverse_mass_matrix = 1. / mass_matrix
                #self.ndim_mass = 1
            else:
                self.mass_matrix = mass_matrix
                self.inverse_mass_matrix = np.linalg.inv(mass_matrix)
            #self.ndim_mass = 2

            
    def define_momentum(self):
        """
        sample momentum
        """
        if self.ndim == 1:
            r = np.random.normal(0, np.sqrt(self.mass_matrix))
        else:
            r = np.random.multivariate_normal(np.zeros(self.ndim), self.mass_matrix)
        return r
    
    def velocity(self, r):
        """
        Get the velocities (gradient of kinetic) given a momentum vector
        """
        if self.ndim == 1:
            v = self.inverse_mass_matrix*r
        else:
            #v = velo(self.inverse_mass_matrix, r)
            v = np.dot(self.inverse_mass_matrix,r)
        return v 

    def kinetic_energy(self, r):
        """
        Get the kinetic energy given momentum
        """
        if self.ndim == 1:
            K = self.inverse_mass_matrix * r**2
        else:
            K = np.dot(r.T, np.dot(self.inverse_mass_matrix, r))
        return 0.5 * K
    
    def leapfrog(self, theta, r, epsilon, size):
        """Perfrom one leapfrog step, updating the momentum and position
        vectors. 
        """
        #update momentum and position vectors
        theta += epsilon * self.velocity(r)
        r1 = - epsilon * self.grad_U(theta,size)
        #r1 = - epsilon * grad_u(self.data,theta,size,self.lnp_grad)
        
        if self.ndim == 1:
            r2 = - epsilon * self.C * self.velocity(r)
            r3 = np.random.normal(0, (2*epsilon*(self.C-self.B))**0.5)
        else:
            r2 = - epsilon * self.C @ self.velocity(r)
            r3 = np.random.multivariate_normal(np.zeros(self.ndim), 2*epsilon*(self.C-self.B))
        r = r + r1 + r2 + r3
        #r = r - 0.5 * epsilon * self.grad_U(size, theta) - epsilon * self.C @ self.velocity(r) + np.random.multivariate_normal(np.zeros(self.ndim), 2*epsilon*(self.C-self.B))
        return theta, r
    
    
    def grad_U(self, thetax, size):
        """
        get the estimate gradient based on minibatches
        
        pramas theta:
            position
            
        pramas size:
            number of datapoints
        """
        if self.usedata:
            df = pd.DataFrame(self.data)
            batch = df.sample(n=size)#,random_state=np.random.RandomState())
            #s = 0
            #for x in batch:
            #    s += self.lnp_grad(x, theta)
            #return -s / size 
            #a = grad_u(self.data, theta, size, self.lnp_grad)
            #return a 
            grad=partial(self.lnp_grad, theta=thetax)
            with multiprocessing.Pool() as pool:
                s = pool.map(grad, np.array(batch))
            return -sum(s)/size
        else:
            return -self.lnp_grad(thetax)
    
    
    def trajectory(self, theta_t, epsilon,length,size):
        
        r_t = self.define_momentum()
        theta0, r0 = theta_t.copy(), r_t.copy()
        #r0 = r_t-0.5*epsilon*self.grad_U(theta0,size)
        
        #update momentum and position vectors
        #theta0 = traj(length, self.leapfrog, theta0, r0, epsilon, size)
        for i in range(length):
            theta_m, r_m = self.leapfrog(theta0,r0,epsilon,size)
            theta0, r0 = theta_m, r_m
        #r0 -= 0.5*epsilon*self.grad_U(theta0,size)
        
        #return theta0
        
        #M-H step
        mu = np.random.uniform(size=1)
        p = np.exp(-self.U(theta0)-self.kinetic_energy(r0) + self.U(theta_t) + self.kinetic_energy(r_t))
        if mu < min(1,p):
            return theta0
        else:
            return theta_t
    
    def U(self, thetax):        
        #s = 0
        #for x in self.data:
        #    s += self.lnp(x, theta)
        #return -s / self.n
        if self.usedata:
            prob=partial(self.lnp, theta=thetax)
            with multiprocessing.Pool() as pool:
                s = pool.map(prob, self.data)
            return -sum(s)/self.n
        else:
            return -self.lnp(thetax)
    
    def sampling(self, iterations, epsilon, length, size):
        """
        sample theta for distribution
        
        pramas iterations:
            number of sampling (trajectory)
        
        params epsilon:
            stepsize for the leapfrog
        
        params length:
            number of leapfrog
            
        params size:
            the size of minibatches
        """
        #setup sampling storage
        thetacurr = self.theta0
        
        # loop over trajectories
        for t in range(iterations):
            temp = self.trajectory(thetacurr, epsilon, length,size)
            self.res.append(temp)
            thetacurr = temp