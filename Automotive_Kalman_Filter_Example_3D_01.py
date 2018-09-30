import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import numpy.random as random
from numpy import dot

"""
Fk, the state-transition model;
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
		
		
		