import numpy as np

def likelihood(x, theta):
	"""Returns likelihood function of model at
	specific values of parameters.
	
	Parameters:
	x: instance of Data21cm object
	theta: model parameters (tuple)
	
	"""
	#first unpack parameters
	a_0, a_1, a_2, a_3, a_4, A, tau, nu_0, w, sig = theta
	nu_c = 75 #center of band in MHz
	full_data = x.full_data #all data 
	processed_data = full_data.loc[full_data[' Weight']==1]
	frequency = processed_data.iloc[:,0].values
	measured_temps = processed_data.iloc[:,2].values
	
	def T_F(a_0, a_1, a_2, a_3, a_4, frequency):
		red_nu = frequency/nu_c
		t_1 = a_0*(red_nu)**(-2.5)
		t_2 = a_1*(red_nu)**(-2.5)*np.log(red_nu)
		t_3 = a_2*(red_nu)**(-2.5)*np.log(red_nu)**2
		t_4 = a_3*(red_nu)**(-4.5)
		t_5 = a_4*(red_nu)**(-2)
		t_f = t_1 + t_2 + t_3 + t_4 + t_5
		return t_f
		
	def T_21(A, tau, nu_0, w, frequency):
		B = 4*(frequency-nu_0)**2/(w**2)
		top = -A*(1-np.exp(-tau*np.exp(B)))
		bottom = 1-np.exp(-tau)
		T_21 = top/bottom
		return T_21
	
	mod = T_F(a_0, a_1, a_2, a_3, a_4, frequency) + T_21(A, tau, nu_0, w, frequency)
	data = measured_temps
	resid_sq = (mod-data)**2
	chi_sq = np.sum(resid_sq)/(sig**2)
	likelihood = np.exp(-chi_sq/2)
	return likelihood
	
