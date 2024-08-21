import numpy as np



temperature = 300  # Example temperature in Kelvin

energies = np.loadtxt('energy.dat')

beta = 1 / (temperature)
boltzmann_factors = np.exp(-beta * np.array(energies))
#print( np.exp(-beta * np.array(energies)))
boltzmann_weights = boltzmann_factors / np.sum(boltzmann_factors)
    
    
print(boltzmann_weights)
