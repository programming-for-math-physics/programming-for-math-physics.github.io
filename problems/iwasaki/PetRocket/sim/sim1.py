
import visual
import math
import sys

# Standard Pressure [Pa]
ST_PRESSURE = 101325

# Air Heat Capacity Ratio
HEAT_CAPACITY_RATIO = 1.4

# PET Radius [m]
PET_RADIUS = 0.045

# PET Height [m]
PET_HEIGHT = 1500.0 / 1000000 / math.pi / PET_RADIUS / PET_RADIUS

# PET Pressure Max [Pa]
PET_PRESSURE = 0.6 * 1000 * 1000

# PET Capacity [m3]
PET_CAPACITY =1.5 / 1000

# PET Nozzle Radius [m]
PET_NOZZLE_RADIUS = 0.004

# Rocket Drag Coefficient
ROCKET_CD = 0.51

# Gravity [m/s2]
GRAVITY = 9.8

# Rocket Mass [kg]
ROCKET_MASS = 0.15

# Water Density [kg/m3]
WATER_DENSITY = 997.062

# Air Density [kg/m3]
AIR_DENSITY = 1.166

# m/s
EARTH_SPEED = 29.78 * 1000 * 0

# SECOND PER FRAME
SPF = 0.25 / 30.0
STEP_DIV = 1000

# SHOW SCALE
VIEWSCALE = 0.2

# m3
pet_water = 0 
# m
pet_pos = (0.0, 0.0)
# m/s
pet_vel = (0.0, 0.0)
# m/s2
pet_acc = (0.0, 0.0)
# Pa
pet_pressure = PET_PRESSURE
# kg/m3
pet_air_density = 0

def sim_setup(angle):
	global pet_water
	global pet_pos
	global pet_vel
	global pet_acc
	global pet_pressure
	global pet_air_density
	global pet_default_angle
	global pet_default_water
	pet_default_water = 1.0 / 1000
	pet_water = pet_default_water
	pet_pos = (0.0, 0.0)
	pet_default_angle = angle
	pet_vel = (math.cos(angle) * 0.001, math.sin(angle) * 0.001)
	pet_acc = (0.0, 0.0)
	pet_pressure = PET_PRESSURE
	pet_air_density = AIR_DENSITY * (pet_pressure / ST_PRESSURE)

def sim_step():
	global pet_water
	global pet_pos
	global pet_vel
	global pet_acc
	global pet_pressure
	global pet_air_density
	global pet_default_angle
	global pet_default_water
	global time
	
	delta_t = SPF / STEP_DIV
	theta = math.atan2(pet_vel[1], pet_vel[0])
	F = 0
	A = PET_NOZZLE_RADIUS * PET_NOZZLE_RADIUS * math.pi
	A0 = PET_RADIUS * PET_RADIUS * math.pi

	if(pet_water > 0):
		# water
		water_height = pet_water / A0
		v_water_sq = (GRAVITY * water_height * math.cos(theta) + ((pet_pressure - ST_PRESSURE) / WATER_DENSITY)) / ((1 - A * A / (A0 * A0)) * 0.5)
		beta_water = math.sqrt(v_water_sq) * A * WATER_DENSITY
		F = beta_water * math.sqrt(v_water_sq)

		original_pet_water = pet_water
		flag = 0
		if(beta_water / WATER_DENSITY * delta_t > pet_water):
			pet_water = 0
			flag = 1
		else:
			pet_water -= beta_water / WATER_DENSITY * delta_t
		#update
		original_pet_pressure = pet_pressure
		pet_pressure = pet_pressure * (PET_CAPACITY - original_pet_water) / (PET_CAPACITY - pet_water)
		pet_air_density = pet_air_density * math.pow(pet_pressure / original_pet_pressure, 1 / HEAT_CAPACITY_RATIO)
	else:
		# air
		P0_airmax = math.pow(2 / (HEAT_CAPACITY_RATIO + 1.0), HEAT_CAPACITY_RATIO / (HEAT_CAPACITY_RATIO - 1)) * pet_pressure
		P0_dash = 0
		v_air = 0
		if(P0_airmax > ST_PRESSURE):
			P0_dash = P0_airmax
			v_air = math.sqrt(2 * HEAT_CAPACITY_RATIO / (HEAT_CAPACITY_RATIO + 1) * pet_pressure / pet_air_density)
		else:
			P0_dash = ST_PRESSURE
			if(pet_pressure > ST_PRESSURE):
				v_air = math.sqrt(2 * HEAT_CAPACITY_RATIO / (HEAT_CAPACITY_RATIO - 1) * (pet_pressure / pet_air_density - ST_PRESSURE / pet_air_density / math.pow(ST_PRESSURE / pet_pressure, 1 / HEAT_CAPACITY_RATIO)))
			else:
				v_air = 0
		F = A * (P0_dash - ST_PRESSURE) + pet_air_density * A * v_air * v_air

		#update
		original_pet_air_density = pet_air_density
		pet_air_density -= pet_air_density * math.pow(P0_dash / pet_air_density, 1 / HEAT_CAPACITY_RATIO) * A * v_air * delta_t / PET_CAPACITY
		pet_pressure = pet_pressure * math.pow(pet_air_density / original_pet_air_density, HEAT_CAPACITY_RATIO)
		# original_pet_pressure = pet_pressure
		# pet_pressure = (PET_CAPACITY - math.pow(P0_dash / pet_pressure, 1 / HEAT_CAPACITY_RATIO) * A * v_air * delta_t) / PET_CAPACITY * pet_pressure
		# pet_air_density = pet_air_density * math.pow(pet_pressure / original_pet_pressure, 1 / HEAT_CAPACITY_RATIO)
	
	pet_vel_len_sq = (pet_vel[0] ** 2 + pet_vel[1] ** 2)
	R = 0.5 * AIR_DENSITY * pet_vel_len_sq * A0 * ROCKET_CD
	pet_acc_F_len = F / (ROCKET_MASS + pet_water * WATER_DENSITY)
	pet_acc_R_len = -R / (ROCKET_MASS + pet_water * WATER_DENSITY)
	pet_acc = (pet_acc_R_len * math.cos(theta) + pet_acc_F_len * math.cos(pet_default_angle), pet_acc_R_len * math.sin(theta) + pet_acc_F_len * math.cos(pet_default_angle) -GRAVITY)
	# if(time >= 0.2):
	# 	pet_acc = (pet_acc_len * math.cos(theta), pet_acc_len * math.sin(theta) - GRAVITY)
	pet_vel = (pet_vel[0] + pet_acc[0] * delta_t, pet_vel[1] + pet_acc[1] * delta_t)
	pet_pos = (pet_pos[0] + pet_vel[0] * delta_t, pet_pos[1] + pet_vel[1] * delta_t)
	
argv = sys.argv
argc = len(argv)

counter = 0
visual.sphere(radius = 0.0001, pos = (1000 * VIEWSCALE, 1000 * VIEWSCALE))
visual.sphere(radius = 0.0001, pos = (1000 * VIEWSCALE, -1000 * VIEWSCALE))

rocket_ = visual.sphere(color = visual.color.red, radius = 40 * VIEWSCALE)

sim_setup(30 / 180.0 * math.pi)

time = 0
while(1):
	if(counter % 20 == 0):
		rocket = visual.sphere(color = visual.color.red, radius = 40 * VIEWSCALE)
		rocket.pos = (pet_pos[0], pet_pos[1])
	if(counter % 30 == 0):
		vel = math.sqrt(pet_vel[0] ** 2 + pet_vel[1] ** 2)
		print(str(time) +"[s]: " + str(pet_pressure) + "[Pa], " + str(vel) + "[m/s], (x, y) = (" + str(pet_pos[0]) + ", " + str(pet_pos[1]) + ")")
		print(str(pet_air_density / AIR_DENSITY))

	for i in range(0, STEP_DIV):
		sim_step()
	time += SPF
	visual.rate(1/SPF)
	counter += 1
	
	if(time > 0.5 and pet_pos[1] < -0.1):
		break


