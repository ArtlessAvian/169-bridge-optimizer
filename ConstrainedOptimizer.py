from UnconstrainedOptimizer import ConjugateGradientDescent
from Bridge import Bridge
from Problem import Problem

class ConstrainedOptimizer:
    def __init__(self, g, h):
        # Lagrange multipliers
        self.lam = [[0 for _ in range(len(h[i]))] for i in range(len(h))]
        self.mu = [[0 for _ in range(len(g[i]))] for i in range(len(g))]
        # Penalty parameters
        self.rg = [1 for _ in range(len(g))]
        self.rh = [1 for _ in range(len(h))]

    def penalty_function(self, vec, func, g, h):
        g_penalty,h_penalty = 0,0

        for i in range(len(g)):
            for j in range(len(g[i])):
                g_penalty += self.mu[i][j] * g[i][j] + self.rg[i]/2 * (max(0, g[i][j]))**2

        for i in range(len(h)):
            for j in range(len(h[i])):
                h_penalty += self.lam[i][j] * h[i][j] + self.rh[i]/2 * h[i][j]**2

        return func(vec) + g_penalty + h_penalty

    def step(self, vec, func, g, h, a=2, e=1e-4):
        T = lambda x: self.penalty_function(x, func, g, h)
        G = lambda x: calculate_gradient(x, T)
        # Use unconstrained optimizer on penalty function
        cgd = ConjugateGradientDescent(G, vec)
        print(T(vec))
        while True:
            vec_old = vec
            vec = cgd.step(T, G, vec)
            if abs(T(vec_old) - T(vec)) < e:
                break

        # Update mu
        for i in range(len(g)):
            for j in range(len(self.mu[i])):
                self.mu[i][j] += max(0, self.rg[i] * g[i][j])

        # Update lambda
        for i in range(len(h)):
            for j in range(len(self.lam[i])):
                self.lam[i][j] += self.rh[i] * h[i][j]

        # Update r
        # Right now all r values are the same; if we keep it this way i'll make self.r a single number instead of arrays
        for i in range(len(self.rg)):
            self.rg[i] *= a
        for i in range(len(self.rh)):
            self.rh[i] *= a

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
    easy_gradient = lambda vec : [2 * vec[0] + vec[1], 2 * vec[1] + vec[0]]
    print("Expecting 27 and [9, 9]")
    print(easy_function([3, 3]))
    print(easy_gradient([3, 3]))

    print()
    print("Should optimize to (3, 3)")

    def g_func(x):
        return [-x[i] + 3 for i in range(len(x))]

    def h_func(x):
        return [x[0] + x[1] - 1]

    small_test = ConstrainedOptimizer([], [h_func([-20, 21])])
    point = [-20, 21]
    for i in range(15):
        print(i)
        #print(point)
        point = small_test.step(point, easy_function, [], [h_func(point)])

    print(point)
    print("End")

    '''
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

    optimizer = ConjugateGradientDescent(the_gradient, vec)
    for i in range(10):
        vec = optimizer.step(the_function, the_gradient, vec)
    # end example usage

    print()
    print("Final Objective Function")
    print(bridge.objective_function())
    '''