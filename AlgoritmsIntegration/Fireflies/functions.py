import numpy as np
from Fireflies.testfunc import *

def starting_points(num_worms, dims):
    return np.random.rand(num_worms,2) * (dims[1]-dims[0]) + dims[0]


#######################################

