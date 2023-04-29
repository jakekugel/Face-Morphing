import numpy as np
import random
import math

def array_info(array):
    result = {}
    if isinstance(array, np.ndarray):
        result['is_numpy_array'] = True
        result['shape'] = array.shape
        result['dtype'] = array.dtype
        result['max'] = array.max()
        result['min'] = array.min()
        # result['order'] = array.order
    else:
        result['is_numpy_array'] = False

    return result


