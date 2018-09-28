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
	
	
