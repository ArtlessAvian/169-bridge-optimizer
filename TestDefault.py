import FrontEnd
from Bridge import Bridge
from Problem import Problem
from ConstrainedOptimizer import ConstrainedOptimizer
import matplotlib.pyplot as plt

if __name__ == "__main__":
    bridge = Bridge(2, 3)

    problem = Problem(bridge)

    the_function = problem.objective_function
    the_constraint = problem.inequality_constraints

    optimizer = ConstrainedOptimizer()

    plt.figure(figsize=(12, 9))

    FrontEnd.print_plot(bridge, 0)

    max_iterations = 30
    vec = bridge.to_vector()

    for i in range(1, max_iterations+1):
        old = the_function(vec)
        vec = optimizer.step(vec, the_function, the_constraint)
        FrontEnd.print_plot(bridge, i)
        if abs(old - the_function(vec)) < 1e-4:
            FrontEnd.print_plot(bridge,-1)
            break