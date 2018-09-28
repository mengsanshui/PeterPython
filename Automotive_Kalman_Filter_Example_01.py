from __future__ import print_function, division
import matplotlib.pyplot as plt
import bar_plot
import numpy as np

# This is just simple 1 dimension Kalman Filer define
class KalmanFilter1D:
	def __init__(self, x0, P, R, Q):
		"""
		x: Initial state
		P: Variance of the state
		R: Measurement error
		Q: Movement error
		Measurement is usually named z
		Movement is usually called u
		
		"""
		self.x = x0
		self.P = P
		self.R = R
		self.Q = Q
	def update(self, z):
		self.x = (self.P * z + self.x * self.R) / (self.P + self.R)
		self.P = 1. / (1./self.P + 1./self.R)
	def predict(self, u=0.0):
		self.x += u
		self.P += self.Q
	# Detail explain	
	def multiply(mu1, var1, mu2, var2):
		mean = (var1*mu2 + var2*mu1) / (var1+var2)
		variance = 1 / (1/var1 + 1/var2)
		return (mean, variance)
	def update_01(mean, variance, measurement, measurement_variance):
		return multiply(mean, variance, measurement, measurement_variance)
	
#This is an example to ues KalmanFilter1D
def volt(temp_variance):
	return random.randn()*temp_variance + 10.3

temp_variance = 2.13**2
movement_error = .2
movement = 0
N=50
zs = [volt(temp_variance) for i in range(N)]
ps = []
estimates = []

kf = KalmanFilter1D(x0=25, # initial state
		    P = 1000, # initial variance - large says 'who knows?'
		    R=temp_variance, # sensor noise
		    Q=movement_error) # movement noise

for i in range(N):
	kf.predict(movement)
	kf.update(zs[i])
	# save for latter plotting
	estimates.append(kf.x)
	ps.append(kf.P)

# plot the filter output and the variance
plt.scatter(range(N), zs, marker='+', s=64, color='r', label='measurements')
plt.plot(estimates, label='filter')
plt.legend(loc='best')
plt.xlim((0,N));plt.ylim((0,30))
plt.show()
plt.plot(ps)
plt.title('Variance')
plt.show()

