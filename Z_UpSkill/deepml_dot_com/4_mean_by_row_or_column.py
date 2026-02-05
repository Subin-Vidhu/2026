def calculate_matrix_mean_(matrix: list[list[float]], mode: str) -> list[float]:
    if not matrix or not matrix[0]:
        return []

    cols = len(matrix[0])
    if any(len(row) != cols for row in matrix):
        return []

    if mode == 'row':
        return [sum(row) / cols for row in matrix]

    if mode == 'column':
        return [sum(col) / len(matrix) for col in zip(*matrix)]

    raise ValueError("Mode must be 'row' or 'column'")


print(calculate_matrix_mean_([[1, 2, 3], [4, 5, 6]], "row"))    # Output: [2.0, 5.0]
print(calculate_matrix_mean_([[1, 2, 3], [4, 5, 6]], "column")) # Output: [2.5, 3.5, 4.5]

def calculate_matrix_mean(matrix: list[list[float]], mode: str) -> list[float]:
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    # Optional: guard against jagged matrices
    for row in matrix:
        if len(row) != cols:
            return []

    means = []

    if mode == "row":
        for row in matrix:
            means.append(sum(row) / cols)

    elif mode == "column":
        for j in range(cols):
            col_sum = 0
            for i in range(rows):
                col_sum += matrix[i][j]
            means.append(col_sum / rows)

    else:
        return []

    return means

# Example usage:
print(calculate_matrix_mean([[1, 2, 3], [4, 5, 6]], "row"))    # Output: [2.0, 5.0]
print(calculate_matrix_mean([[1, 2, 3], [4, 5, 6]], "column")) # Output: [2.5, 3.5, 4.5]