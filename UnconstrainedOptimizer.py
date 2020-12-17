import math
from Bridge import Bridge
from Problem import Problem
import numpy as np

class HookJeeves:
    def __init__(self):
        pass

    def step(self, func, vec, alpha = 10, epsilon = 1e-4, gamma = 0.5):
        y, n = func(vec), len(vec)
        while alpha > epsilon:
            #print(f"Alpha: {alpha}")
            improved = False
            x_best, y_best = vec, y
            for i in range(n):
                basis = np.array([(1 if j == i else 0) for j in range(len(vec))])
                for sign in [-1, 1]:
                    new_vec = vec + sign * alpha * basis
                    new_y = func(new_vec)

                    if(new_y < y_best):
                        x_best, y_best, improved = new_vec, new_y, True
               
            vec, y = x_best, y_best

            if not improved:
                alpha *= gamma
        return vec


if __name__ == "__main__":
    print("### EASY TESTS ###")

    easy_function = lambda vec : vec[0] ** 2 + vec[1] ** 2 + vec[0] * vec[1]

    print("Should optimize to (0, 0)")
    small_test = HookJeeves()
    point = [-20, 21]
    for i in range(5):
        print(point)
        point = small_test.step(easy_function, point)
    print(point)
    print()
    
    print("### ACTUAL USAGE ###")

    # the actual problem
    bridge = Bridge()
    bridge.randomize()

    vec = bridge.to_vector()
    problem = Problem(bridge)

    print("Original Objective Function")
    print(bridge.objective_function())

    # example usage of optimizer
    the_function = problem.objective_function
    the_gradient = lambda veccc : calculate_gradient(veccc, problem.objective_function)

    #optimizer = ConjugateGradientDescent(the_gradient, vec)
    optimizer = HookJeeves()
    for i in range(10):

        vec = optimizer.step(the_function, vec)
    # end example usage

    print()
    print("Final Objective Function")
    print(bridge.objective_function())
    
