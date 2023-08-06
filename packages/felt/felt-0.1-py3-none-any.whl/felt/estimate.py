from .matrix import Matrix, Vector



def estimate(paths, movements, movement_flows):
    incidence_matrix = Matrix([
        [
            movement.incidence_count(path)   
            for path in paths
        ]
        for movement in movements
    ])
    return furness(incidence_matrix, movement_flows)


def furness(A, b):
    A = Matrix(A)
    b = Vector(b)

    current_x = Vector.ones(A.shape[1])
    
    for _ in range(100):
        for i in range(len(b)):
            current_b = A @ current_x
            ratio = b[i] / current_b[i]
            current_x[A[i] != 0] = current_x * ratio

    return current_x


            



    







