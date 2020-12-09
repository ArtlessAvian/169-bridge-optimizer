class ConstrainedOptimizer:
    def __init__(self, g, h):
        # Need to update this
        self.lam = [[0 for _ in range(len(h[i]))] for i in range(len(h))]
        self.mu = [[0 for _ in range(len(g[i]))] for i in range(len(g))]
        self.r = [0 for _ in range(len(h)+len(g))]

    def penalty_function(self, vec, func, g, h):
        g_penalty,h_penalty = 0,0

        g_i = g(vec)
        active = self.active_constraints()
        for i in range(len(g_i)):
            if g_i[i] in active:
                for j in range(len(vec)):
                    g_penalty += self.mu[i][j] * g_i[i][j] + self.r[1]/2 * g[i][j]**2
            else:
                for j in range(len(vec)):
                    g_penalty += self.r[2]/2 * (max(0, g[i][j]))**2

        h_i = h(vec)
        for i in range(len(h_i)):
            for j in range(len(vec)):
                h_penalty += self.lam[i][j] * h[i][j] + self.r[0]/2 * h[i][j]**2

        return func(vec) + g_penalty + h_penalty

    def penalty_gradient(self, vec, func, g, h):
        pass

    def active_constraints(self):
        return []

    def step(self, vec, func, g, h, a=2):
        T = lambda x: self.penalty_function(x, func, g, h)
        G = lambda x: self.penalty_gradient(x, func, g, h)
        # Use unconstrained optimizer on penalty function
        # vec = unconstrained_optimizer(vec, T, G)

        # Update lambda
        h_i = h(vec)
        for i in range(len(h_i)):
            for j in range(len(self.lam[i])):
                self.lam[i][j] += self.r[0] * h_i[i][j]

        # Update mu
        g_i = g(vec)
        active = self.active_constraints()
        for i in range(len(g_i)):
            if g_i[i] in active:
                for j in range(len(self.mu[i])):
                    self.mu[i][j] += self.r[1] * g_i[i][j]
                    if self.mu[i][j] < 0:
                        self.mu[i][j] = 0
            else:
                for j in range(len(self.mu[i])):
                    if g_i[i][j] <= 0:
                        self.mu[i][j] = 0
                    else:
                        self.mu[i][j] = self.r[2] * g_i[i][j]

        # Update r
        for i in range(len(self.r)):
            self.r[i] *= a

        return vec