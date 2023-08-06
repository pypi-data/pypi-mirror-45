class hmc():
    def __init__(self,data,lnp,lnp_grad,initialguess, M = None):
        '''
        
        '''
        self.data = data 
        self.ndim = len(initialguess)
        self.get_mass_matrix(M)
        self.theta0 = initialguess
        self.lnp = lnp
        self.lnp_grad = lnp_grad
        self.res = []
        self.n = len(data)

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
            v = self.inverse_mass_matrix * r
        else:
            v = np.dot(self.inverse_mass_matrix, r)
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
    
    def grad_U(self, theta):
        """
        get the estimate gradient based on minibatches
        
        pramas size:
            number of datapoints
        """
        s = [0] * self.ndim
        for x in self.data:
            s += self.lnp_grad(x, theta)  
        return -s / self.n
    
    def leapfrog(self, theta, r, epsilon):
        """Perfrom one leapfrog step, updating the momentum and position
        vectors. 
        """
        #update momentum and position vectors
        theta += epsilon * self.velocity(r)
        r -= epsilon * self.grad_U(theta)
        #r = r - 0.5 * epsilon * self.grad_U(size, theta) - epsilon * self.C @ self.velocity(r) + np.random.multivariate_normal(np.zeros(self.ndim), 2*epsilon*(self.C-self.B))
        return theta, r
    
    
    
    def trajectory(self, theta_t, epsilon, length):
        r_t = self.define_momentum()
        theta0, r0 = theta_t.copy(), r_t.copy()
        r0 = r_t-0.5*epsilon*self.grad_U(theta0)
        for i in range(length):
            theta_m, r_m = self.leapfrog(theta0,r0,epsilon)
            theta0, r0 = theta_m, r_m
        r0 -= 0.5*epsilon*self.grad_U(theta0)
        
        
        #M-H step
        mu = np.random.uniform(size=1)
        p = np.exp(-self.U(theta0)-self.kinetic_energy(r0) + self.U(theta_t) + self.kinetic_energy(r_t))
        if mu < min(1,p):
            return theta0
        else:
            return None
    
    def U(self, theta):        
        s = 0
        for x in self.data:
            s += self.lnp(x, theta)
        return -s / self.n
    
    
    def sampling(self, iterations, epsilon, length):
        """
        sample theta for distribution
        
        pramas iterations:
            number of sampling (trajectory)
        
        params epsilon:
            stepsize for the leapfrog
        
        params length:
            number of leapfrog
        """
        #setup sampling storage
        thetacurr = self.theta0
        
        # loop over trajectories
        for t in range(iterations):
            temp = self.trajectory(thetacurr, epsilon, length)
            if temp is not None:#len(temp) == self.ndim: #or temp[0] != 0:
                self.res.append(temp)
                thetacurr = temp