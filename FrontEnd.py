from ConstrainedOptimizer import ConstrainedOptimizer
from Bridge import Bridge
from Problem import Problem
import numpy as np
import matplotlib.pyplot as plt

MAX = 20

def print_plot(bridge, i):
    for j, (a, b) in enumerate(bridge.members):
        x = [bridge.nodes[a][0], bridge.nodes[b][0]]
        y = [bridge.nodes[a][1], bridge.nodes[b][1]]
        # print(bridge.edge_width[j])
        plt.plot(x,y, label = str(round(bridge.edge_width[j], 3)))
        # plt.pause(0.05)
    plt.title(bridge.objective_function())
    plt.legend(loc="upper left", bbox_to_anchor=(1,1))
    plt.pause(0.05)
    if i == -1 or i == MAX-1:
        plt.savefig("Bridges/bridge_final.")
        plt.show()
    else:
        plt.savefig("Bridges/bridge_" + str(i) +".png")
        plt.clf()


if __name__ == "__main__":
    # the problem
    bridge = Bridge(3, 2)
    bridge.randomize()

    vec = bridge.to_vector()
    problem = Problem(bridge)

    print("Original Objective Function")
    print(bridge.objective_function())

    # example usage of optimizer
    the_function = problem.objective_function
    the_constraint = problem.inequality_constraints
    optimizer = ConstrainedOptimizer()

    plt.figure(figsize=(12,9))

    for i in range(MAX):
        old = the_function(vec)
        vec = optimizer.step(vec, the_function, the_constraint)
        print_plot(bridge, i)
        if abs(old - the_function(vec)) < 1e-4:
            print(f"done! {i}")
            print_plot(bridge,-1)
            break
