import numpy as np
import matplotlib.pyplot as plt

Cp = 31.5  # kj/k
E = 830.85  # kJ
Max_dT = 26.38  # K

Starting_Temp = np.linspace(85, 95, 10)
RXN_fin = np.linspace(2, 20, 19)

m = Max_dT/(RXN_fin**2)
dT_dt = (m*RXN_fin**2-m*(RXN_fin+0.01)**2) / 0.01  # in K/m

kW_array = dT_dt*Cp/60  # K/min * kj/K * 1 min / 60 s = kJ/s = kW
print(RXN_fin)
print(np.round(-kW_array,1))
print(np.round(E/RXN_fin/60,1))
print(np.round(-kW_array*4,1))
print(np.round(E/RXN_fin/60*4,1))
#for m in m_array:
#    plt.plot(t, m*t**2 + 85)

#plt.ylim((85,85+26.38))
#plt.show()