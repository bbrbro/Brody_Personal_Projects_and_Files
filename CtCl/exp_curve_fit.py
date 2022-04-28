import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

x_array = np.linspace(20,60,11)

x = np.array([40,44,50,60])
y = np.array([950,600,250,90])/60

plt.plot(x, y, '.')
plt.title("Original Data")

def monoExp(x, m, k, b):
    return m * np.exp(-k * x) + b

# perform the fit
p0 = (2000, .1, 50) # start with values near those we expect
params, cv = scipy.optimize.curve_fit(monoExp, x, y, p0)
m, t, b = params
sampleRate = 20_000 # Hz
tauSec = (1 / t) / sampleRate

# determine quality of the fit
squaredDiffs = np.square(y - monoExp(x, m, t, b))
squaredDiffsFromMean = np.square(y - np.mean(y))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"R² = {rSquared}")

# plot the results
plt.plot(x, y, '.', label="data")
plt.plot(x_array, monoExp(x_array, m, t, b), '--', label="fitted")
plt.title("Fitted Exponential Curve")

for x,y in list(zip(x_array,monoExp(x_array, m, t, b))):
    print(x,",",y)


plt.show()

# inspect the parameters
print(f"Y = {m} * e^(-{t} * x) + {b}")
print(f"Tau = {tauSec * 1e6} µs")