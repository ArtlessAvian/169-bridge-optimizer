from ConstrainedOptimizer import ConstrainedOptimizer
from Bridge import Bridge
from Problem import Problem
from time import time
import random


random.seed(1)

if __name__ == "__main__":

    n_tests = 100
    bridge_sizes = [(2,3), (3,4), (4,5)]
    for n_main, n_other in bridge_sizes:
        start_cost = []
        end_cost = []
        n_iters = []
        total_time = []
        feasible = 0
        for _ in range(n_tests):
            iterations = 0
            start = time()

            bridge = Bridge(n_main, n_other)
            bridge.randomize()

            vec = bridge.to_vector()
            problem = Problem(bridge)

            start_cost.append(bridge.objective_function())

            the_function = problem.objective_function
            the_constraint = problem.inequality_constraints
            optimizer = ConstrainedOptimizer()

            for i in range(1,31):
                old = the_function(vec)
                vec = optimizer.step(vec, the_function, the_constraint)
                iterations+=1
                if abs(old - the_function(vec)) < 1e-4:
                    break

            end = time()
            total_time.append(end-start)
            end_cost.append(bridge.objective_function())
            n_iters.append(iterations)
            feasible += all(i > 0 for i in bridge.inequality_min_length())

        print(f"Statistics for Bridge n_main={n_main}, n_other={n_other}")
        print()

        print(f"Average Cost: {sum(end_cost) / n_tests}")
        print(f"Average Decrease in Cost: {(sum(start_cost) - sum(end_cost)) / n_tests}")
        print(f"Average Iterations (Constrained): {sum(n_iters) / n_tests}")
        print(f"Number of Feasible Bridges: {feasible} / {n_tests}")
        print(f"Average Time: {sum(total_time) / n_tests}")
        print("-------------------------------------------------------")