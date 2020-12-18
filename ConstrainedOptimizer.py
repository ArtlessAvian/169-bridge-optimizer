from UnconstrainedOptimizer import HookJeeves
from Bridge import Bridge
from Problem import Problem
import numpy as np

class ConstrainedOptimizer:
    def __init__(self):
        self.r = 100
        pass

    # Returns the penalty.
    def penalty_function(self, vec, ineq_constr):
        sum_penalty = 0

        g = ineq_constr(vec)
        for penalty in g:
            sum_penalty += max(-penalty, 0)

        return sum_penalty

    def step(self, vec, func, ineq_constr, a=1.1, epsilon=1e-4):
        T = lambda x: func(x) + self.penalty_function(x, ineq_constr) * self.r
        # Use unconstrained optimizer on penalty function
        unconstrained = HookJeeves()
        for _ in range(30):
            vec_old = vec
            vec = unconstrained.step(T, vec)

        self.r *= a
        return vec


if __name__ == "__main__":
    # print("### EASY TESTS ###")

    # easy_function = lambda vec : vec[0] ** 2 + vec[1] ** 2 + vec[0] * vec[1]
    # print("Should optimize to (3, 3)")

    # def inequality(x):
    #     return x - 3

    # point = np.array([-3, 21])
    # small_test = ConstrainedOptimizer()

    # for i in range(10):
    #     print(f"step {i}: {point}, {easy_function(point)}")
    #     point = small_test.step(point, easy_function, inequality)

    # print(point)
    # print("End")
    # input()
    # print()
    print("### ACTUAL USAGE ###")

    # the actual problem
    bridge = Bridge(2, 3)
    # bridge.randomize()

    vec = bridge.to_vector()
    problem = Problem(bridge)

    bridge.print_desmos_copypaste()

    print("Original Objective Function")
    print(bridge.objective_function())

    # example usage of optimizer
    the_function = problem.objective_function
    the_constraint = problem.inequality_constraints
    optimizer = ConstrainedOptimizer()

    for i in range(20):
        old = the_function(vec)
        vec = optimizer.step(vec, the_function, the_constraint)
        bridge.print_plot(i)
        if abs(old - the_function(vec)) < 1e-4:
            print(f"done! {i}")
            bridge.print_plot(-1)
            break

    # end example usage

    print()
    print("Final Objective Function")
    print(bridge.objective_function())
    print(bridge.inequality_max_stress())
    print(all(i > 0 for i in bridge.inequality_max_stress()))
    bridge.print_desmos_copypaste()
