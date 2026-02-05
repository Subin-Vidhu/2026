def matrix_dot_vector(a: list[list[int|float]], b: list[int|float]) -> list[int|float]:
  # Return a list where each element is the dot product of a row of 'a' with 'b'.
  # If the number of columns in 'a' does not match the length of 'b', return -1.
  # Edge case: empty matrix
    if not a or not a[0]:
        return -1

    # Number of columns in matrix
    cols = len(a[0])

    # Check dimension compatibility
    if cols != len(b):
        return -1

    result = []

    for row in a:
        # Optional safety check for jagged matrices
        if len(row) != cols:
            return -1

        dot_product = 0
        for i in range(cols):
            dot_product += row[i] * b[i]

        result.append(dot_product)

    return result
print(matrix_dot_vector([[1, 2, 3], [4, 5, 6]], [7, 8, 9]))