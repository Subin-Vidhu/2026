def inverse_2x2(matrix: list[list[float]]) -> list[list[float]] | None:
    a, b = matrix[0][0], matrix[0][1]
    c, d = matrix[1][0], matrix[1][1]
    
    determinant = a * d - b * c
    
    if determinant == 0:
        return None
    
    inverse = [
        [d / determinant, -b / determinant],
        [-c / determinant, a / determinant]
    ]
    return inverse

matrix = [[4, 7], [2, 6]]
inverse = inverse_2x2(matrix)
if inverse:
    print(inverse)  # Output: [[0.6, -0.7], [-0.2, 0.4]]