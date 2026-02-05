import numpy as np

def reshape_matrix(a: list[list[int|float]], new_shape: tuple[int, int]) -> list[list[int|float]]:
    #Write your code here and return a python list after reshaping by using numpy's tolist() method
    try:
        arr = np.array(a)
        reshaped_matrix = arr.reshape(new_shape)
        return reshaped_matrix.tolist()
    except ValueError:
        return []

print(reshape_matrix([[1, 2, 3], [4, 5, 6]], (3, 2)))

# or

import numpy as np

def reshape_matrix(a: list[list[int|float]], new_shape: tuple[int|float]) -> list[list[int|float]]:
    # Not compatible case
    if len(a)*len(a[0]) != new_shape[0]*new_shape[1]:
        return []
    return np.array(a).reshape(new_shape).tolist()
