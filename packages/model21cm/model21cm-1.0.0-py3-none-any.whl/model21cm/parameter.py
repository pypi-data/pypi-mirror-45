import pandas as pd
import numpy as np


class parameter: 

    def __init__(self, name=None, uniform_min=None, uniform_max=None): 
        self.name=name
        if (not uniform_min==None) and (not uniform_max==None): 
            self.set_uniform_prior(uniform_min, uniform_max)

    def set_uniform_prior(self, parameter_min, parameter_max): 
        """Returns uniform probability density over specified range."""
        if parameter_max > parameter_min:
            self.prior = uniform(parameter_min, parameter_max)
        else: 
            raise Exception("Error: second input must be larger than first.")

    def set_jeffreys_prior(self, parameter_min, parameter_max):
        """Returns Jeffreys pdf over specified range.""" 
        if parameter_min>0 and parameter_max>0 and parameter_max>parameter_min: 
           self.prior = jeffreys(parameter_min, parameter_max)
        else: 
            raise Exception("Error: Invalid choice of max/min for Jeffreys Prior.")

    def prior_at(self, x): 
        """Returns value of prior at x."""
        if hasattr(self, 'prior'): 
            return self.prior(x)
        else: 
            raise Exception("Error: no prior set on this parameter.")

    def logprior_at(self, x):
        """Returns value of log of prior at x."""
        if hasattr(self, 'prior'):
            p = self.prior(x)
            if p==0: 
                return -np.inf
            else: 
                return np.log(p)
        else:
            raise Exception("Error: no prior set on this parameter.")


def uniform(parameter_min, parameter_max): 
    """Returns uniform prior for specified range."""
    const = 1. / (parameter_max - parameter_min)
    
    def uniform_at(x):
        """Helper for uniform( function.""" 
        if x<parameter_min or x>parameter_max: 
            return 0. 
        else:  
            return const 
    return uniform_at

def jeffreys(parameter_min, parameter_max): 
    """Returns the Jeffreys prior for specified range."""
    const = 1. / np.log(parameter_max / parameter_min)

    def jeffreys_at(x): 
        """Helper for jeffreys( function."""
        if x<parameter_min or x>parameter_max: 
            return 0.
        else: 
            return const / x

    return jeffreys_at
