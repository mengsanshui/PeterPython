import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import numpy.random as random
from numpy import dot

"""
Fk, the state-transition model; F is always a matrix of constants
Hk, the observation model;
Qk, the covariance of the process noise;
Rk, the covariance of the observation noise;
Bk, the control-input model, for each time-step

in general residual is the difference between prediction and measurement
Use Kalman gain to update estimate where between the measured position and the predicted position
1. predict the next value for x with "x + vel*time"
2. get measurement for x
3. compute residual as: "x - x_prediction"
4. compute kalman gain based on noise levels
5. compute new position as "residual * kalman gain"

x = dot(F, x) + dot(B, u)
P = dot(F, P).dot(F.T) + Q
y = z - dot(H, x)
S = dot(H, P).dot(H.T) + R
K = dot(P, H.T).dot(np.linalg.inv(S))
x = x + dot(K,y)
P = (I - dot(K, H)).dot(P)

"""
class KalmanFilter:
	def __init__(self, dim_x, dim_z, dim_u=0):
		""" 
		Parameters:
		dim_x : int
		Number of state variables for the Kalman filter. For example, if
		you are tracking the position and velocity of an object in two
		dimensions, dim_x would be 4.
		This is used to set the default size of P, Q, and u
		
		dim_z : int
		Number of measurement inputs. For example, if the sensor
		provides you with position in (x,y), dim_z would be 2.
		
		dim_u : int (optional)
		size of the control input, if it is being used.
		Default value of 0 indicates it is not used.
		"""
		self.x = np.zeros((dim_x,1)) # state
		self.P = np.eye(dim_x) # uncertainty covariance
		self.Q = np.eye(dim_x) # process uncertainty
		self.u = np.zeros((dim_x,1)) # motion vector
		self.B = 0 # control transition matrix
		self.F = 0 # state transition matrix
		self.H = 0 # Measurement function
		self.R = np.eye(dim_z) # state uncertainty
		
		# identity matrix. Do not alter this.
		self._I = np.eye(dim_x)
	
		
	def update(self, Z, R=None):
		"""
		Add a new measurement (Z) to the kalman filter. If Z is None, nothing is changed.
		Parameters:
		Z : np.array measurement for this update.
		R : np.array, scalar, or None Optionally provide R to override the measurement noise for this
			one call, otherwise self.R will be used.
		"""
		# In real world you can invoke Z = read_sensor() then update(self, Z, R)
		if Z is None:
			return
		if R is None:
			R = self.R
		elif np.isscalar(R):
			R = np.eye(self.dim_z) * R
		
		# error (residual) between measurement and prediction
		y = Z - dot(H, x)
		# project system uncertainty into measurement space
		S = dot(H, P).dot(H.T) + R
		# map system uncertainty into kalman gain
		K = dot(P, H.T).dot(linalg.inv(S))
		# predict new x with residual scaled by the kalman gain
		self.x = self.x + dot(K, y)
		
		I_KH = self._I - dot (K, H)
		self.P = dot(I_KH).dot(P).dot(I_KH.T) + dot(K, R).dot(K.T)
		
		
	def predict(self, u=0):
		""" 
		Predict next position.
		Parameters:
		u : np.array Optional control vector. If non-zero, it is multiplied by B
		to create the control input into the system.
		"""
		self.x = dot(self.F, self.x) + dot(self.B, u)
		self.P = self.F.dot(self.P).dot(self.F.T) + self.Q
		
	
class TestSensor(object):
	def __init__(self, x0=0, velocity=1, noise=0.0):
		""" x0 - initial position
		velocity - (+=right, -=left)
		noise - scaling factor for noise, 0== no noise
		"""
		self.x = x0
		self.velocity = velocity
		self.noise = math.sqrt(noise)
	def sense(self):
		self.x = self.x + self.velocity
		return self.x + random.randn() * self.noise	


def Q_DWPA(dim, dt=1., sigma=1.):
	""" Returns the Q matrix for the Discrete Wiener Process Acceleration Model.
	dim may be either 2 or 3, dt is the time step, and sigma is the variance in
	the noise"""
	assert dim == 2 or dim == 3
	if dim == 2:
	Q = np.array([[.25*dt**4, .5*dt**3],
	             [ .5*dt**3, dt**2]], dtype=float)
	else:
		Q = np.array([[.25*dt**4, .5*dt**3, .5*dt**2],
					 [ .5*dt**3, dt**2, dt],
					 [ .5*dt**2, dt, 1]], dtype=float)
	return Q * sigma
		
def Test_tracking_filter(R,Q=0,cov=1.):
	Test_filter = KalmanFilter (dim_x=2, dim_z=1)
	Test_filter.x = np.array([[0],[0]]) # initial state (location and velocity)
	Test_filter.F = np.array([[1,1],[0,1]]) # state transition matrix
	Test_filter.H = np.array([[1,0]]) # Measurement function
	Test_filter.R *= R # measurement uncertainty
	Test_filter.P *= cov # covariance matrix
	if np.isscalar(Q):
		Test_filter.Q = Q_DWPA(2, sigma=Q)
	else:
		Test_filter.Q = Q
	return Test_filter

def filter_position(noise=0, count=0, R=0, Q=0, P=500., data=None, initial_x=None):
	""" Kalman filter 'count' readings from the TestSensor.
	'noise' is the noise scaling factor for the TestSensor.
	'data' provides the measurements. If set, noise will
	be ignored and data will not be generated for you.
	returns a tuple of (positions, measurements, covariance)
	"""
	if data is None:
		Test = TestSensor(velocity=1, noise=noise)
		zs = [Test.sense() for t in range(count)]
	else:
		zs = data
	Test_filter = Test_tracking_filter(R=R, Q=Q, cov=P)
	if initial_x is not None:
		Test_filter.x = initial_x
	pos = [None] * count
	cov = [None] * count
	for t in range(count):
		z = zs[t]
		pos[t] = Test_filter.x[0,0]
		cov[t] = Test_filter.P
		# perform the kalman filter steps
		Test_filter.update (z)
		Test_filter.predict()
	return (pos, zs, cov)
	
def plot_track(noise=None, count=0, R=0, Q=0, P=500., initial_x=None, data=None, plot_P=True, title='Kalman Filter'):
	ps, zs, cov = filter_position(noise=noise, data=data, count=count,
	R=R, Q=Q, P=P, initial_x=initial_x)
	p0, = plt.plot([0,count],[0,count])
	p1, = plt.plot(range(1,count+1),zs, linestyle='dashed')
	p2, = plt.plot(range(1,count+1),ps)
	plt.legend([p0,p1,p2], ['actual','measurement', 'filter'], loc=2)
	plt.ylim((0-10,count+10))
	plt.title(title)
	plt.show()
	if plot_P:
		plt.subplot(121)
		plot_covariance(cov, (0,0))
		plt.subplot(122)
		plot_covariance(cov, (1,1))
		plt.show()

def plot_covariance(P, index=(0,0)):
	ps = []
	for p in P:
		ps.append(p[index[0],index[1]])
	plt.plot(ps)
		