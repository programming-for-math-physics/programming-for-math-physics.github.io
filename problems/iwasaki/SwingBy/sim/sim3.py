
import math
import sys

# kg
PROBE_MASS = 0.750 * (10 ** 3)

# mmm/kg/ss
G = 6.67384 * (10 ** -11)

# m/s
PROBE_SPEED = 14 * 1000

# m/s
EARTH_SPEED = 29.78 * 1000 

# maximum step [/day]
MAX_STEP_INV = 1 / 3.0

# minimum step [/day]
# MIN_STEP_INV = 1 / 0.0006
MIN_STEP_INV = 1 / 0.0001

# day
CHALLENGE = 365 * 8

# SHOW SCALE
VIEWSCALE = 1.0 / 2000000

day = 0
probe_pos = (0.0, 0.0)
probe_vel = (0.0, 0.0)
probe_acc = (0.0, 0.0)

planet_len = 0
# ecliptic longitude [rad]
planet_e_longitude = []
# revolution radius [m]
planet_r_radius = []
# radius [m]
planet_radius = []
# mass [kg]
planet_mass = []
# revolution period [day]
planet_period = []
# name (string)
planet_name = []

def sim_setup(angle):
	global planet_len
	global planet_e_longitude
	global planet_r_radius
	global planet_radius
	global planet_mass
	global planet_period
	sim_load()

def sim_init_probe(startday, angle):
	global planet_e_longitude
	global planet_r_radius
	global planet_radius
	global planet_mass
	global planet_period
	global probe_pos
	global probe_vel
	global probe_acc
	global day
	day = startday
	earth_pos=(planet_r_radius[0] * math.cos(2 * math.pi * day / planet_period[0] + planet_e_longitude[0]), planet_r_radius[0] * math.sin(2 * math.pi * day / planet_period[0] + planet_e_longitude[0])) 
	earth_radius = planet_radius[0]
	probe_pos = (earth_pos[0] + earth_radius * math.cos(angle), earth_pos[1] + earth_radius * math.sin(angle))
	one_hour = 1.0 / 24
	earth_pos_after=(planet_r_radius[0] * math.cos(2 * math.pi * (day + one_hour) / planet_period[0] + planet_e_longitude[0]), planet_r_radius[0] * math.sin(2 * math.pi * (day + one_hour) / planet_period[0] + planet_e_longitude[0])) 
	probe_vel = (PROBE_SPEED * math.cos(angle) + (earth_pos_after[0] - earth_pos[0]) / 3600, PROBE_SPEED * math.sin(angle) + (earth_pos_after[1] - earth_pos[1]) / 3600)
	# print math.sqrt(((earth_pos_after[0] - earth_pos[0]) / 3600) **2 + ((earth_pos_after[1] - earth_pos[1]) / 3600) ** 2)
	# print math.sqrt(probe_vel[0] ** 2 + probe_vel[1] ** 2)
	probe_acc = (0.0, 0.0)
	
def sim_setup():
	global planet_len
	global planet_name
	global planet_e_longitude
	global planet_r_radius
	global planet_radius
	global planet_mass
	global planet_period
	fp = open("swingbydata.txt", "r")
	index = 0
	for line in fp:
		if(index == 0):
			planet_len = int(line)
		else:
			planet_name.append(line.split("\t")[0].strip())
			planet_e_longitude.append(float(line.split("\t")[2]) * math.pi / 180)
			planet_r_radius.append(float(line.split("\t")[3]) * 1000)
			planet_radius.append(float(line.split("\t")[4]) * 1000 / 2)
			planet_mass.append(float(line.split("\t")[5]) * (10 ** 23))
			planet_period.append(float(line.split("\t")[6]))
			if(index == planet_len):
				break
		index += 1
	fp.close()

def sim_step():
	global planet_len
	global planet_e_longitude
	global planet_r_radius
	global planet_radius
	global planet_mass
	global planet_period
	global probe_pos
	global probe_vel
	global probe_acc
	global day
	global step_inv
	global target_planet_distance
	global target_planet_index
	global nearest_planet_ratio
	# f = GMm/r^2
	force = (0, 0)
	nearest_planet_ratio = 10 ** 15
	for i in range(0, planet_len):
		planet_pos=(planet_r_radius[i] * math.cos(2 * math.pi * day / planet_period[i] + planet_e_longitude[i]), planet_r_radius[i] * math.sin(2 * math.pi * day / planet_period[i] + planet_e_longitude[i])) 
		distance = math.sqrt((probe_pos[0] - planet_pos[0]) ** 2 + (probe_pos[1] - planet_pos[1]) ** 2)
		if(i == target_planet_index):
			target_planet_distance = distance
		planet_ratio = distance / planet_radius[i]
		if(planet_ratio < 1):
			# collision
			if(i == 0):
				if(planet_ratio < 0.95):
					print("HIT:" + planet_name[i])
					return False
			else:
				print("HIT:" + planet_name[i])
				return False
		if(planet_ratio < nearest_planet_ratio):
			nearest_planet_ratio = planet_ratio
		
		force_len = G * (planet_mass[i] / distance) * (PROBE_MASS / distance)
		force = (force[0] + force_len * (planet_pos[0] - probe_pos[0]) / distance, force[1] + force_len * (planet_pos[1] - probe_pos[1]) / distance)
		# print(planet_pos[0]-probe_pos[0], planet_pos[1]-probe_pos[1])
	# exit()
	probe_acc = (force[0] / PROBE_MASS, force[1] / PROBE_MASS)
	probe_vel = (probe_vel[0] + probe_acc[0] / step_inv * 24 * 3600, probe_vel[1] + probe_acc[1] / step_inv * 24 * 3600)
	probe_pos = (probe_pos[0] + probe_vel[0] / step_inv * 24 * 3600, probe_pos[1] + probe_vel[1] / step_inv * 24 * 3600)
	return True

def get_energy():
	global planet_len
	global planet_e_longitude
	global planet_r_radius
	global planet_radius
	global planet_mass
	global planet_period
	global probe_pos
	global probe_vel
	global probe_acc
	global day
	vel = math.sqrt(probe_vel[0] ** 2 + probe_vel[1] ** 2)
	vel_energy = 0.5 * PROBE_MASS * vel * vel
	g_energy = 0
	for i in range(0, planet_len):
		planet_pos=(planet_r_radius[i] * math.cos(2 * math.pi * day / planet_period[i] + planet_e_longitude[i]), planet_r_radius[i] * math.sin(2 * math.pi * day / planet_period[i] + planet_e_longitude[i])) 
		distance = math.sqrt((probe_pos[0] - planet_pos[0]) ** 2 + (probe_pos[1] - planet_pos[1]) ** 2)
		g_energy += - G * planet_mass[i] * PROBE_MASS / distance
	return g_energy + vel_energy
	
argv = sys.argv
argc = len(argv)

if(argc != 7):
	print("sim3.py first_day day_interval search_range angle_division angle_recursive target_planet")
	print("sim3.py 1 10 365 100 3 JUPITER")
	exit()

first_day = int(argv[1])
day_interval = int(argv[2])
search_range = int(argv[3])
angle_division = int(argv[4])
angle_recursive = int(argv[5])
target_planet = argv[6]

start_day = first_day

sim_setup()

# search target_planet_index
target_planet_index = -1
for i in range(0, planet_len):
	if(planet_name[i] == target_planet):
		target_planet_index = i
		break
if(target_planet_index == -1):
	print("invalid target_planet")
	exit()
target_planet_radius = planet_radius[target_planet_index]

# sim_init_probe(0, 0)
# print("default energy = " + str(get_energy() / 1000 / 1000) + "[MJ]")

while(1):
	angle_delta = 2 * math.pi
	angle_candidate = 0
	
	for rec in range(0, angle_recursive):
		max_distance = 0
		max_angle = 0
		max_energy = 0
		max_velocity = 0
		max_near_flag = 0
		nearest_target_planet_distance = 10 ** 20
		for i in range(0, angle_division):
			angle = angle_candidate - angle_delta / 2 + angle_delta * i / angle_division
			near_flag = 0
			sim_init_probe(start_day, angle)
			step_inv = MIN_STEP_INV
			ret = True
			step_counter = 0
			while(day - start_day < CHALLENGE):
				ret = sim_step()
				if(ret == False):
					break
				if(target_planet_distance < target_planet_radius * 100):
					near_flag = 1
				if(near_flag == 1):
					# able to swingby
					if(step_counter % 50 == 0):
						energy = get_energy()
						if(energy > max_energy):
						 	max_angle = angle
							max_distance = math.sqrt(probe_pos[0] ** 2 + probe_pos[1] ** 2)
							max_velocity = math.sqrt(probe_vel[0] ** 2 + probe_vel[1] ** 2)
							max_energy = energy
							max_near_flag = 1
				else:
					if(max_near_flag == 0 and target_planet_distance < nearest_target_planet_distance):
						nearest_target_planet_distance = target_planet_distance
					 	max_angle = angle
						max_velocity = math.sqrt(probe_vel[0] ** 2 + probe_vel[1] ** 2)
					 	max_energy = get_energy()
				step_inv = MIN_STEP_INV / ((nearest_planet_ratio / 10) ** 2)
				if(step_inv < MAX_STEP_INV):
					step_inv  = MAX_STEP_INV
				step_counter += 1
				day += 1.0 / step_inv
			if(ret == False):
				continue
		angle_candidate = max_angle
		angle_delta = angle_delta / angle_division
	if(max_near_flag == 1):
		print ("Approach Succeeded")
		print (str(start_day) + "[day], angle = " + str(max_angle) + ", distance = " + str(max_distance / 1000) + "[km], energy = " + str(max_energy / 1000 / 1000) + "[MJ], speed = " + str(max_velocity / 1000) + "[km/s]")
	else:
		print (str(start_day) + "[day], angle = " + str(max_angle) + ", distance = " + str(nearest_target_planet_distance / 1000) + "[km], energy = " + str(max_energy / 1000 / 1000) + "[MJ] approach ratio = " + str(nearest_target_planet_distance / target_planet_radius) + ", speed = " + str(max_velocity / 1000) + "[km/s]")
	start_day += day_interval
	if(start_day - first_day > search_range):
		break

