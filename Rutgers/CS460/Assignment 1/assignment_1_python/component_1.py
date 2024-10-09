import numpy as NP

def check_SOn(m: NP.ndarray, epsilon: float = 0.01) -> bool:
    if m.shape[0] != m.shape[1]:
        return False
    
    identity_matrix = NP.eye(m.shape[0])
    orthogonality_check = NP.allclose(NP.dot(m.T, m), identity_matrix, atol = epsilon)
    
    determinant_check = NP.isclose(NP.linalg.det(m), 1.0, atol = epsilon)
    
    return orthogonality_check and determinant_check

def check_quaternion(v: NP.array, epsilon: float = 0.01) -> bool:
    if len(v) != 4:
        return False
    
    magnitude_squared = NP.sum(NP.square(v))
    
    return NP.abs(magnitude_squared - 1) < epsilon

def check_SEn(m: NP.ndarray, epsilon: float = 0.01) -> bool:
    n = m.shape[0] - 1
    
    if m.shape[0] != m.shape[1] or n not in [2, 3]:
        return False
    
    rotation_matrix = m[:n, :n]
    
    if not check_SOn(rotation_matrix, epsilon):
        return False
    
    last_row_check = NP.allclose(m[n, :], NP.append(NP.zeros(n), 1), atol = epsilon)
    
    return last_row_check