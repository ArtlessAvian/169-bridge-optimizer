from UnconstrainedOptimizer import HookJeeves
from Bridge import Bridge
from Problem import Problem

class ConstrainedOptimizer:
    def __init__(self, g, h):
        # Penalty parameter
        self.rho = 0.1

    # Returns the penalty.
    def penalty_function(self, vec, g_func, h_func):
        g_penalty = 0

        g = g_func(vec)
        for penalty in g:
            g_penalty += 1/penalty

        return g_penalty/self.rho

    def step(self, vec, func, g_func, h_func, a=2, e=1e-4):
        T = lambda x: func(vec) + self.penalty_function(x, g_func, h_func)
        G = lambda x: calculate_gradient(x, T)
        # Use unconstrained optimizer on penalty function
        cgd = HookJeeves()
        for _ in range(10):
            #print(f"Constrained Step: {_}")
            #input()
            vec_old = vec
            vec = cgd.step(T, vec)
            if abs(T(vec_old) - T(vec)) < e:
                break

        # Update r
        self.rho *= a

        return vec


def calculate_gradient(vec, func, small_step=1e-4):
    gradient = []
    old = func(vec)
    for i in range(len(vec)):
        vec[i] += small_step
        new = func(vec)
        vec[i] -= small_step * 2
        old = func(vec)
        vec[i] += small_step

        partial = (new - old) / small_step / 2
        gradient.append(partial)
    return gradient


if __name__ == "__main__":
    print("### EASY TESTS ###")

    easy_function = lambda vec : vec[0] ** 2 + vec[1] ** 2 + vec[0] * vec[1]

    print("Should optimize to (3, 3)")

    def inequality(x):
        return [x[i] - 3 for i in range(len(x))]

    def equality(x):
        return []

    point = [21, 21]
    small_test = ConstrainedOptimizer(inequality(point), equality(point))
    for i in range(10):
        print(f"step {i}: {easy_function(point)}")
        old = easy_function(point)
        point = small_test.step(point, easy_function, inequality, equality)
        if abs(old - easy_function(point)) < 1e-4:
            break

    print(point)
    print("End")
    input()
    print()
    print("### ACTUAL USAGE ###")

    # the actual problem
    bridge = Bridge(3)
    bridge.randomize()

    vec = bridge.to_vector()
    problem = Problem(bridge)

    print("Original Objective Function")
    print(bridge.objective_function())

    # example usage of optimizer
    the_function = problem.objective_function
    the_gradient = lambda veccc : calculate_gradient(veccc, problem.objective_function)
    optimizer = ConstrainedOptimizer(problem.inequality_constraints(vec), problem.inequality_constraints(vec))

    for i in range(30):
        old = the_function(vec)
        vec = optimizer.step(vec, the_function, problem.inequality_constraints, problem.inequality_constraints(vec))
        print("step ", i)
        input()
        # print(the_function(vec), vec)
        if abs(old - the_function(vec)) < 1e-4:
            break

    # end example usage

    print()
    print("Final Objective Function")
    print(bridge.objective_function())
    bridge.print_desmos_copypaste()