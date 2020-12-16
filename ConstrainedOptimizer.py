from UnconstrainedOptimizer import ConjugateGradientDescent
from Bridge import Bridge
from Problem import Problem

class ConstrainedOptimizer:
    def __init__(self, g, h):
        # Lagrange multipliers
        self.lam = [[0 for _ in range(len(h[i]))] for i in range(len(h))]
        self.mu = [[0 for _ in range(len(g[i]))] for i in range(len(g))]
        # Penalty parameter
        self.r = 1

    def penalty_function(self, vec, func, g_func, h_func):
        g_penalty,h_penalty = 0,0

        g = g_func(vec)
        for i in range(len(g)):
            for j in range(len(g[i])):
                g_penalty += self.mu[i][j] * g[i][j] + self.r/2 * (max(0, g[i][j]))**2

        h = h_func(vec)
        for i in range(len(h)):
            for j in range(len(h[i])):
                h_penalty += self.lam[i][j] * h[i][j] + self.r/2 * h[i][j]**2

        return func(vec) + g_penalty + h_penalty

    def step(self, vec, func, g_func, h_func, a=2, e=1e-4):
        T = lambda x: self.penalty_function(x, func, g_func, h_func)
        G = lambda x: calculate_gradient(x, T)
        # Use unconstrained optimizer on penalty function
        cgd = ConjugateGradientDescent(G, vec)
        while True:
            vec_old = vec
            vec = cgd.step(T, G, vec)
            if abs(T(vec_old) - T(vec)) < e:
                break

        # Update mu
        g = g_func(vec)
        for i in range(len(g)):
            for j in range(len(self.mu[i])):
                self.mu[i][j] += max(0, self.r * g[i][j])

        # Update lambda
        h = h_func(vec)
        for i in range(len(h)):
            for j in range(len(self.lam[i])):
                self.lam[i][j] += self.r * h[i][j]

        # Update r
        self.r *= a

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
        return [[-x[i] + 3 for i in range(len(x))]]

    def equality(x):
        return []

    point = [-15, 21]
    small_test = ConstrainedOptimizer(inequality(point), equality(point))
    for i in range(100):
        old = easy_function(point)
        point = small_test.step(point, easy_function, inequality, equality)
        if abs(old - easy_function(point)) < 1e-4:
            break

    print(point)
    print("End")

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
    optimizer = ConstrainedOptimizer(problem.inequality_constraints(vec), problem.equality_constraints(vec))

    for i in range(1000):
        old = the_function(vec)
        vec = optimizer.step(vec, the_function, problem.inequality_constraints, problem.equality_constraints)
        # print("step ", i)
        # print(the_function(vec), vec)
        if abs(old - the_function(vec)) < 1e-4:
            break

    # end example usage

    print()
    print("Final Objective Function")
    print(bridge.objective_function())
    bridge.print_desmos_copypaste()