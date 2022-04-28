import numpy as np
import matplotlib.pyplot as plt



tank_size = 12# L or kg
cp_water = 4.18 #kj/kg/k
kw_heater = 3 #kw

temp_profile = np.array([22,23.5,27,30,32.5,35,37,39,41,42.5,43.5,44.5,45.0,46,46.5,47.0,47.5,47.5,48.0,48.0,48.5,49.0,49.0,49.0,49.0,49.0])
time_profile = np.linspace(0,len(temp_profile)-1,len(temp_profile))

rxn_mass = np.array([2195,450,260])/1000 #in kg
rxn_cp = np.array([1.4,1.68,2.4])#kj/kg/k
dt_array = (temp_profile[1:]-temp_profile[:-1])
rxn_power = sum(rxn_mass*rxn_cp)*dt_array/60 #currently in kj/s or kw
print(rxn_power)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (min)')
ax1.set_ylabel('Temp in C', color=color)
ax1.plot(time_profile, temp_profile, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Power in kW', color=color)  # we already handled the x-label with ax1
ax2.plot(time_profile[1:], rxn_power, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

water_change = (sum(rxn_mass*rxn_cp)*25)/(cp_water*tank_size) # should by in (kj / kj/k) goes to k
print(water_change)

water_change = (sum(rxn_mass*rxn_cp)*25)/(cp_water*8) # should by in (kj / kj/k) goes to k
print(water_change)

print(sum(rxn_mass*rxn_cp))