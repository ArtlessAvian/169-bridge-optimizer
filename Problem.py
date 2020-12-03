import math

from Bridge import Bridge

class Problem:
    def __init__(self, left, right, other = [], n_main = 3, n_free = 3):
        self.bridge = Bridge(2 + len(other), n_main, n_free)
        
        self.fixed = [left, right]
        self.fixed.extend(other)

    def objective_function(self):
        cost = 0

        for i in range(len(self.bridge.free)):
            
            for j in range(i + 1, len(self.bridge.free)):
                dist = distance(self.bridge.free[i], self.bridge.free[j])
                cost += dist * self.bridge.get_edge_to_free(i, j)

            for j in range(len(self.bridge.main)):
                dist = distance(self.bridge.free[i], self.bridge.main[j])
                cost += dist * self.bridge.get_edge_to_main(i, j)

            for j in range(len(self.fixed)):
                dist = distance(self.bridge.free[i], self.fixed[j])
                cost += dist * self.bridge.get_edge_to_fixed(i, j)

        cost += distance(self.fixed[0], self.bridge.main[0])
        for i in range(len(self.bridge.main) - 1):
            cost += distance(self.bridge.main[i], self.bridge.main[i+1])
        cost += distance(self.bridge.main[len(self.bridge.main)-1], self.fixed[1])

        return cost
    
    def equality_constraints(self):
        return 0

    def inequality_constraints(self):
        return 0

def distance(point, other):
    dx = point[0] - other[0]
    dy = point[1] - other[1]
    return math.sqrt(dx * dx + dy * dy)

if __name__ == "__main__":
    problem = Problem((-10, 0), (10, 0))
    step = 0.0001

    # This will work once someone writes from_vector()
    gradient = []

    old = problem.objective_function()
    vec = problem.bridge.to_vector()

    for i in range(len(vec)):
        vec[i] += step
        problem.bridge.from_vector(vec)
        vec[i] -= step

        new = (problem.objective_function())
        partial = (new - old) / h
        gradient.append(partial)

    print(gradient)

    # print(problem.objective_function())
    
    # problem.bridge.main[0] = (-h, 0)
    # print(problem.objective_function())


    
