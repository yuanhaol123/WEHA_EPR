import numpy as np
import sys
energy = np.loadtxt("energy.dat", usecols=[8,9], skiprows=0)
sub = energy[0] - energy[1]
mult = sub *4.18
np.savetxt(sys.stdout, mult)

