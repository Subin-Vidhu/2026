def transpose_matrix(a: list[list[int | float]]) -> list[list[int | float]]:
    if not a or not a[0]:
        return []

    rows = len(a)
    cols = len(a[0])

    # Optional: ensure matrix is not jagged
    for row in a:
        if len(row) != cols:
            return []

    result = []

    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(a[i][j])
        result.append(new_row)

    return result

print(transpose_matrix([[1, 2], [3, 4], [5, 6]]))
print(transpose_matrix([[1, 2, 3], [4, 5, 6]]))