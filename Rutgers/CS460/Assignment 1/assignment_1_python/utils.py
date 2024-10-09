import numpy as NP
import matplotlib.pyplot as PLT
from mpl_toolkits.mplot3d import Axes3D

def quaternion_to_rotation_matrix(q: NP.array) -> NP.ndarray:
    # Quaternion elements.
    q0, q1, q2, q3 = q
    
    # Rotation matrix from quaternion.
    rotation_matrix = NP.array(
        [
            [1 - 2 * (q2 ** 2 + q3 ** 2), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
            [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 ** 2 + q3 ** 2), 2 * (q2 * q3 - q0 * q1)],
            [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 ** 2 + q2 ** 2)]
        ]
    )
    
    return rotation_matrix

def visualize_rotation(m: NP.ndarray):
    # Define initial vectors (North pole and a nearby point).
    v0 = NP.array([0, 0, 1]) # North pole.
    epsilon = 1e-2 # small perturbation
    v1 = NP.array([0, epsilon, 1]) # a point slightly displaced.
    
    # Apply the rotation.
    v0_prime = m @ v0 # rotate v0
    v1_prime = m @ v1 - v0 # rotate v1 and subtract v0 to get the direction.
    
    # Create a sphere for visualization.
    fig = PLT.figure()
    ax = fig.add_subplot(111, projection = '3d')
    
    # Create a sphere mesh.
    u = NP.linspace(0, 2 * NP.pi, 100)
    v = NP.linspace(0, NP.pi, 100)
    x = NP.outer(NP.cos(u), NP.sin(v))
    y = NP.outer(NP.sin(u), NP.sin(v))
    z = NP.outer(NP.ones(NP.size(u)), NP.cos(v))
    
    # Plot the sphere.
    ax.plot_surface(x, y, z, color = 'lightblue', alpha = 0.3, rstride = 5, cstride = 5)
    
    # Plot the original vector v0 (North pole).
    ax.quiver(0, 0, 0, v0[0], v0[1], v0[2], color = 'blue', label = 'v0')
    
    # Plot the original vector v1.
    ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color = 'orange', label = 'v1') 
    
    # Plot the rotated vector v0_prime.
    ax.quiver(0, 0, 0, v0_prime[0], v0_prime[1], v0_prime[2], color ='red', label = 'v0_prime')
    
    # Plot the rotated vector v1_prime (a point slightly displaced).
    ax.quiver(v0_prime[0], v0_prime[1], v0_prime[2], v1_prime[0], v1_prime[1], v1_prime[2], color = 'green', label = 'v1_prime')
    
    # Add labels and legend.
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.legend()
    
    # Show the plot.
    PLT.show()