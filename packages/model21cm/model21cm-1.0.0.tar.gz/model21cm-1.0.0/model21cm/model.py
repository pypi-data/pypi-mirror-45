import numpy as np

class model:

    def __init__(self, name=None):
        self.name=name 

    def add_parameters(self, parameterlist):
        """Adds parameters and their priors to model."""
        self.globalprior = priorfunction(parameterlist)
        self.parameters=[]
        for i in parameterlist: 
            self.parameters.append(i.name)

    def add_data(self, freq, temp):
        """Adds dataset to model."""
        self.loglikelihood = loglikelihoodfunction(freq, temp)
        self.frequencies = freq
        self.temperatures = temp

    def globalprior_at(self, x): 
        """Returns global prior value at sample point."""
        return self.globalprior(x)

    def globallogprior_at(self, x): 
        """Returns log of global prior value at sample point."""
        p = self.globalprior(x)
        if p==0: 
            return -np.inf
        else: 
            return np.log(p)

    def loglikelihood_at(self, x): 
        """Returns log of global likelihood at sample point."""
        return self.loglikelihood(x)

    def logposterior_at(self, x): 
        """Returns log of global posterior at sample point."""
        value = self.globallogprior_at(x) + self.loglikelihood_at(x)
        if not np.isfinite(value):
            return -np.inf
        else: 
            return value  




def priorfunction(parameterlist): 
    """Generates global prior using given parameters."""
    #Note that this function, likelihood, and posterior all have precarious depenence on 
    #parameter ordering at the moement. Fix. 
    def priorvalue(x): 
        """Helper for priorfunction( ."""
        value = 1.
        for i in range(np.size(parameterlist)): 
            value = value * parameterlist[i].prior_at(x[i])
        return value
    return priorvalue

def loglikelihoodfunction(freq, temp):
    """Generates global likelihood for default model using given dataset.""" 
    def loglikelihoodvalue(x):
        #Note this requires x to have a specific parameter ordering. Potential for mistakes. Fix.  
        a0, a1, a2, a3, a4, A, tau, nu0, w = x
        N = np.size(freq)
        sig = 0.1 #Make this a model parameter to marginalize later. 

        def foreground(a0, a1, a2, a3, a4, freq): 
            """Returns foreground contribution to model."""
            nu_c = 77 #Verify this
            red_nu = freq/nu_c
            t1 = a0*(red_nu)**(-2.5)
            t2 = a1*(red_nu)**(-1.5)
            t3 = a2*(red_nu)**(-0.5)
            t4 = a3*(red_nu)**(0.5)
            t5 = a4*(red_nu)**(1.5)
            tf = t1 + t2 + t3 + t4 + t5
            return tf

        def signal(A, tau, nu0, w, freq):
            """Returns 21-cm signal contribution to model."""
            B = 4*((freq-nu0)**2)*np.log(-1/tau*np.log((1+np.exp(-tau))/2))*(1/w**2)
            top = -A*(1-np.exp(-tau*np.exp(B)))
            bottom = 1-np.exp(-tau)
            T_21 = top/bottom
            return T_21

        model = foreground(a0, a1, a2, a3, a4, freq) + signal(A, tau, nu0, w, freq)
        resid_sq = (temp - model)**2
        chi_sq = np.sum(resid_sq/(sig**2))
        log_like = -0.5*chi_sq
        return log_like
    return loglikelihoodvalue






















