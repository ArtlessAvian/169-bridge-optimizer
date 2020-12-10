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
                h_penalty += self.lam[i][j] * h[i][j] + self.rh[0]/2 * h[i][j]**2

        return func(vec) + g_penalty + h_penalty

    def step(self, vec, func, g, h, unconstr_opt, a=2):
        T = lambda x: self.penalty_function(x, func, g, h)
        # Use unconstrained optimizer on penalty function
        vec = unconstr_opt(vec, T)

        # Update mu
        for i in range(len(g)):
            for j in range(len(self.mu[i])):
                self.mu[i][j] += max(0, self.r[1] * g[i][j])

        # Update lambda
        for i in range(len(h)):
            for j in range(len(self.lam[i])):
                self.lam[i][j] += self.r[0] * h[i][j]

        # Update r
        # Right now all r values are the same; if we keep it this way i'll make self.r a single number instead of arrays
        for i in range(len(self.rg)):
            self.rg[i] *= a
        for i in range(len(self.rh)):
            self.rh[i] *= a

        return vec