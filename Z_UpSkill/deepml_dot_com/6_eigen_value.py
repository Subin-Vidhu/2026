import math

def calculate_eigenvalues(matrix: list[list[float | int]]) -> list[float]:
    # Validate 2x2 matrix
    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        raise ValueError("Input must be a 2x2 matrix")

    a, b = matrix[0]
    c, d = matrix[1]

    trace = a + d
    determinant = a * d - b * c

    discriminant = trace**2 - 4 * determinant

    # For real eigenvalues (as expected in this problem)
    sqrt_disc = math.sqrt(discriminant)

    lambda1 = (trace + sqrt_disc) / 2
    lambda2 = (trace - sqrt_disc) / 2

    # Sort from highest to lowest
    return sorted([lambda1, lambda2], reverse=True)

matrix = [[2, 1], [1, 2]]
print(calculate_eigenvalues(matrix))  # Output: [3.0, 1.0]