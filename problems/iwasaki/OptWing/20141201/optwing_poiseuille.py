
import math
import numpy as np
import scipy as sp
import scipy.sparse
from scipy.sparse.linalg import spsolve
from scipy.sparse.linalg import lsqr
from scipy.linalg import lstsq
from scipy.linalg import solve
from scipy import io
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm


from numpy.linalg import matrix_rank

# Standard Pressure [Pa]
ST_PRESSURE = 101325

# Air Density [kg/m3]
AIR_DENSITY = 1.165

# Air Viscosity [Pas]
AIR_VISCOSITY = 1.869 * (10 ** -5)

# Air Kinematic Viscosity [m2s]
AIR_K_VISCOSITY = 1.604 * (10 ** -5) 
WATER_K_VISCOSITY = 0.00089

# Velocity [m/s]
OBJECT_VELOCITY_U = 0
OBJECT_VELOCITY_V = 0

VECTOR_DIV = 1

# (i, j) is a grid point.
def isinobject(i, j):
	global N, M
	# return (i < N * 0.3 and j < M * 0.2) or (i < N * 0.1)
	# return (i - N / 2) ** 2 + (j - M / 2) ** 2 < ( ( M + N )/16) ** 2
	# return i > N * 0.2 and i < N * 0.4 and j > M * 0.4 and j < M * 0.6
	return False

def nearpindices(i, j):
	global N, M
	_i = max(min(i, N-1), 0)
	_j = max(min(j, M-1), 0)
	if isinobject(_i, _j):
		ret =[]
		if _i-1 >=0 and not isinobject(_i-1, _j):
			ret.append((_i-1, _j))
		if _j-1 >=0 and not isinobject(_i, _j-1):
			ret.append((_i, _j-1))
		if _i+1 < N and not isinobject(_i+1, _j):
			ret.append((_i+1, _j))
		if _j+1 < M and not isinobject(_i, _j+1):
			ret.append((_i, _j+1))
		return ret
	else:
		return [(_i, _j)]

def getp(i, j):
	global N, M, p
	if(i == 0):
		return ST_PRESSURE + ST_PRESSURE * (10 ** -8)
	if(i == N - 1):
		return ST_PRESSURE
	pindices = nearpindices(i, j)
	pressure = 0
	for (pi, pj) in pindices:
		pressure += p[pi, pj] / len(pindices)
	return pressure

def getu(_u, i, j):
	global N, M
	if(i == 0): # left
		return _u[1, j]
		# return OBJECT_VELOCITY_U
	if(i == N): # right
		return _u[N - 1, j]
		# return OBJECT_VELOCITY_U
	return _u[i, j]

def getv(_v, i, j):
	global N, M
	if(j == 0): # top
		#return _v[i, 1]
		return OBJECT_VELOCITY_V
	if(j == N): # bottom
		#return _v[i, M - 1]
		return OBJECT_VELOCITY_V
	return _v[i, j]

def init():
	global u, v, p
	global up, vp, Dp, _Dp, pp
	global p_dict
	global Poisson
	global deltat, deltax, deltay
	global constant_p_index
	global time
	# width of p elements
	global N
	# height of p elements
	global M
	
	deltax=0.002
	deltay=0.002
	deltat=0.05
	M = 10
	N = 50
	time = 0
	
	constant_p_index = (0, 0)
	
	# make poisson ... POISSON * p' = D'
	row_length = 0
	p_dict = {}
	for i in range(0, N):
		for j in range(0, M):
			if(not isinobject(i, j)):
				if( not (i == 0) and not (i == N - 1)):
				# if( not (i == 0 and j == M / 2) and not (i == N - 1 and j == M / 2)):
					p_dict[i + j * N] = row_length
					row_length += 1
	print ("p_num = " + str (row_length))
	_Poisson = sp.sparse.lil_matrix((row_length, row_length))

	for i in range(0, N):
		for j in range(0, M):
			if(i + j * N in p_dict):
				setpoissonij(i-1, j, _Poisson, p_dict[i + j * N], p_dict, (1  / (deltax ** 2)) * deltat)
				setpoissonij(i  , j, _Poisson, p_dict[i + j * N], p_dict, (-2 / (deltax ** 2)) * deltat)
				setpoissonij(i+1, j, _Poisson, p_dict[i + j * N], p_dict, (1  / (deltax ** 2)) * deltat)
				setpoissonij(i, j-1, _Poisson, p_dict[i + j * N], p_dict, (1  / (deltay ** 2)) * deltat)
				setpoissonij(i, j  , _Poisson, p_dict[i + j * N], p_dict, (-2 / (deltay ** 2)) * deltat)
				setpoissonij(i, j+1, _Poisson, p_dict[i + j * N], p_dict, (1  / (deltay ** 2)) * deltat)
	Poisson = _Poisson.tocsr()
	#print (Poisson.todense())
	#print matrix_rank(Poisson.todense())
	# Poisson = _Poisson.todense()
	u  = np.zeros((N+1, M))
	v  = np.zeros((N, M+1))
	p  = np.zeros((N, M))
	up = np.zeros((N+1, M))
	vp = np.zeros((N, M+1))
	Dp = np.zeros((N * M))
	_Dp= np.zeros((row_length))
	pp = np.zeros((N * M))
	
	#initialize up and vp
	for i in range(0, N+1):
		for j in range(0, M):
			up[i, j] = OBJECT_VELOCITY_U
			u[i, j]  = OBJECT_VELOCITY_U
	for i in range(0, N):
		for j in range(0, M+1):
			vp[i, j] = OBJECT_VELOCITY_V
			v[i, j]  = OBJECT_VELOCITY_V
	for i in range(1, N):
		for j in range(1, M-1):
			up[i, j] = 0
			u[i, j]  = 0
	for i in range(1, N-1):
		for j in range(1, M):
			vp[i, j] = 0
			v[i, j]  = 0
	# initialize p
	for i in range(0, N):
		for j in range(0, M):
			p[i, j] = ST_PRESSURE
	# fix boundary
	for i in range(0, N):
		for j in range(0, M):
			if isinobject(i, j):
				u[i, j] = 0
				u[i+1, j] = 0
				v[i, j] = 0
				v[i, j+1] = 0

def setpoissonij(i, j, _poisson, row, p_dict, value):
	global N, M
	pindices = nearpindices(i, j)
	for (pi, pj) in pindices:
		if (pi + pj * N) in p_dict:
			_poisson[row, p_dict[pi + pj * N]] += value / len(pindices)
	
def mainstep():
	global u
	global v
	global p
	global up
	global vp
	global Dp
	global _Dp
	global pp
	global p_dict
	global Poisson
	global deltat
	global deltax
	global deltay
	global N
	global M
	
	# update up
	for i in range(1, N):
		for j in range(1, M-1):
			up_A_x = (((getu(u, i+1, j) + getu(u, i, j)) / 2) ** 2 - ((getu(u, i, j) + getu(u, i-1, j)) / 2) ** 2) / deltax 
			up_A_y = ((getu(u, i, j+1) + getu(u, i, j)) * (getv(v, i, j+1) + getv(v, i-1, j+1)) - (getu(u, i, j-1) + getu(u, i, j)) * (getv(v, i, j) + getv(v, i-1, j))) / (deltay * 4)
			up_B = (getu(u, i-1, j) - 2 * getu(u, i, j) + getu(u, i+1, j)) / (deltax ** 2) + (getu(u, i, j-1) - 2 * getu(u, i, j) + getu(u, i, j+1)) / (deltay ** 2)
			up[i, j] = getu(u, i, j) + deltat * (- (getp(i, j) - getp(i-1, j)) / (AIR_DENSITY * deltax) - up_A_x - up_A_y + AIR_K_VISCOSITY * up_B)
	# update vp
	for i in range(1, N-1):
		for j in range(1, M):
			vp_A_y = (((getv(v, i, j) + getv(v, i, j+1)) / 2) ** 2 - ((getv(v, i, j-1) + getv(v, i, j)) / 2) ** 2) / deltay
			vp_A_x = ((getu(u, i+1, j-1) + getu(u, i+1, j)) * (getv(v, i, j) + getv(v, i+1, j)) - (getu(u, i, j-1) + getu(u, i, j)) * (getv(v, i-1, j) + getv(v, i, j))) / (deltax * 4)
			vp_B = (getv(v, i-1, j) - 2 * getv(v, i, j) + getv(v, i+1, j)) / (deltax ** 2) + (getv(v, i, j-1) - 2 * getv(v, i, j) + getv(v, i, j+1)) / (deltay ** 2)
			vp[i, j] = getv(v, i, j) + deltat * (- (getp(i, j) - getp(i, j-1)) / (AIR_DENSITY * deltay) - vp_A_x - vp_A_y + AIR_K_VISCOSITY * vp_B)
	# update Dp
	for i in range(0, N):
		for j in range(0, M):
			Dp[i + j * N] = (getu(up, i+1, j) - getu(up, i, j)) / deltax + (getv(vp, i, j+1) - getv(vp, i, j)) / deltay
	#		print (i, j, Dp[i + j * N], Dp[i + (M - 1 - j) * N])
			if (i + j * N) in p_dict:
				_Dp[p_dict[i + j * N]] = Dp[i + j * N]
	# symmetry check
	#for i in range(0, N):
	#	for j in range(0, M):
	#		#if(math.fabs(Dp[i + j * N] - Dp[i + (M - 1 - j) * N]) > 0.001):
	#		print (i, j, Dp[i + j * N], Dp[i + (M - 1 - j) * N])
	
	# solve pp
	# _pp = spsolve(Poisson, _Dp)
	ret = lsqr(Poisson, _Dp)
	_pp = ret[0]
	
	#print _pp
	
	print ("error = " + str(ret[3]))
	
	row = 0
	for i in range(0, N):
		for j in range(0, M):
			if i + j * N in p_dict:
				pp[i + j * N] = _pp[row]
				row += 1
			else:
				pp[i + j * N] = 0
	
	# update u
	for i in range(1, N):
		for j in range(1, M-1):
			u[i, j] = getu(up, i, j) - deltat * (pp[i+j*N] - pp[(i-1)+j*N]) / deltax
	# update v
	for i in range(1, N-1):
		for j in range(1, M):
			v[i, j] = getv(vp, i, j) - deltat * (pp[i+j*N] - pp[i+(j-1)*N]) / deltay
			
	u_array = []
	for j in range(0, M/2):
		u_array.append(u[N/2, j])
	print u_array
	# update Dp
	for i in range(0, N):
		for j in range(0, M):
			Dp[i + j * N] = (getu(u, i+1, j) - getu(u, i, j)) / deltax + (getv(v, i, j+1) - getv(v, i, j)) / deltay
	#for i in range(0, N):
	#	for j in range(0, M):
	#		print (i, j, Dp[i + j * N], Dp[i + (M - 1 - j) * N])
	
	# update p
	for i in range(0, N):
		for j in range(0, M):
			p[i, j] += (pp[i + j * N] / AIR_DENSITY)
	
	# fix boundary
	for i in range(0, N):
		for j in range(0, M):
			if isinobject(i, j):
				u[i, j] = 0
				v[i, j] = 0
				u[i+1, j] = 0
				v[i, j+1] = 0

init()
pltu = np.zeros((M/VECTOR_DIV, N/VECTOR_DIV))
pltv = np.zeros((M/VECTOR_DIV, N/VECTOR_DIV))
pltp = np.zeros((M/VECTOR_DIV, N/VECTOR_DIV))

def pltstep(num):
	global pltu
	global pltv
	global pltp
	global N
	global M
	global u
	global v
	global time
	fig.clear()
	
	for i in range(0, 5):
		time += deltat
		mainstep()

	if False:
		(X,Y) = np.meshgrid([i+0.5 for i in range(0, N/VECTOR_DIV)],[i+0.5 for i in range(0, M/VECTOR_DIV)])
		for i in range(0, N, VECTOR_DIV):
			for j in range(0, M, VECTOR_DIV):
				pltu[i/VECTOR_DIV, j/VECTOR_DIV] = (u[i,j] + u[i+1,j]) / 2
				pltv[i/VECTOR_DIV, j/VECTOR_DIV] = (v[i,j] + v[i,j+1]) / 2
		plt.quiver(X, Y , pltu, pltv)
	else:
		(X,Y) = np.meshgrid([i for i in range(0, N/VECTOR_DIV+1)],[i for i in range(0, M/VECTOR_DIV+1)])
		for i in range(0, N, VECTOR_DIV):
			for j in range(0, M, VECTOR_DIV):
				if isinobject(i, j):
					pltp[j/VECTOR_DIV, i/VECTOR_DIV] = 0
				else:
					pltp[j/VECTOR_DIV, i/VECTOR_DIV] = getp(i, j) - ST_PRESSURE
		plt.pcolor(X, Y, pltp, cmap=cm.Greens)
		plt.colorbar()
	
		(X,Y) = np.meshgrid([i+0.5 for i in range(0, N/VECTOR_DIV)],[i+0.5 for i in range(0, M/VECTOR_DIV)])
		for i in range(0, N, VECTOR_DIV):
			for j in range(0, M, VECTOR_DIV):
				pltu[j/VECTOR_DIV, i/VECTOR_DIV] = (getu(u, i, j) + getu(u, i+1, j)) / 2
				pltv[j/VECTOR_DIV, i/VECTOR_DIV] = (getv(v, i, j) + getv(v, i, j+1)) / 2
		plt.quiver(X, Y, pltu, pltv)
		
		plt.xlim(-1, N/VECTOR_DIV+1)
		plt.ylim(-1, M/VECTOR_DIV+1)
		
	fig.suptitle(str(time), fontweight="bold")
fig = plt.figure()
anim = animation.FuncAnimation(fig, pltstep , interval = 10)
plt.show()
