# def scalar_multiply(matrix: list[list[int|float]], scalar: int|float) -> list[list[int|float]]:
#     return [[element * scalar for element in row] for row in matrix]



# scalar_mul([[1,2,3]], 5)
def scalar_mul(a, scalar):
    if not a:
        return -1
    final_arr = []
    for row in a:
        row_arr = []
        for element in row:
            row_arr.append(element * scalar)
        final_arr.append(row_arr)
    return final_arr

print(scalar_mul([[1,2,3]], 5))