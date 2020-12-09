import random
import math

def distance(point, other):
    dx = point[0] - other[0]
    dy = point[1] - other[1]
    return math.sqrt(dx * dx + dy * dy)

class Bridge:
    def __init__(self, left = (-10, 0), right = (10, 0), other = [], n_main = 2, n_other = 3):
        self.fixed = [left, right]
        self.fixed.extend(other)
        
        self.n_main = n_main
        # The first n_main are main joints.
        self.free = [(0, 0) for i in range(n_main + n_other)]
    
        # TODO: Reduce wasted space
        # [free] x [free U fixed]
        self.edges = [[0 for j in range(len(self.fixed) + len(self.free))] for i in range(len(self.free))]

        self.road_cost_per_length = 10 # Temporary

    def objective_function(self):
        strut_cost = 0

        # Sum all struts.
        for i in range(len(self.free)):
            for j in range(i + 1, len(self.free)):
                dist = distance(self.free[i], self.free[j])
                strut_cost += dist * max(0, self.get_edge_to_free(i, j))

            for j in range(len(self.fixed)):
                dist = distance(self.free[i], self.fixed[j])
                strut_cost += dist * max(0, self.get_edge_to_fixed(i, j))

        # Sum road. (left to main, main to main, main to right)
        road_length = 0
        road_length += distance(self.fixed[0], self.free[0])
        for i in range(self.n_main):
            road_length += distance(self.free[i], self.free[i+1])
        road_length += distance(self.free[self.n_main-1], self.fixed[1])

        road_cost = road_length * self.road_cost_per_length

        return strut_cost + road_cost

    def equality_constraints(self):
        return 0

    def inequality_constraints(self):
        return 0

    # Vector Conversion

    def to_vector(self):
        vec = []
        for point in self.free:
            vec.extend(point)
        for row in self.edges:
            vec.extend(row)
        return vec
    
    def from_vector(self, vec):
        for i in range(len(self.free)):
            self.free[i] = (vec[2 * i], vec[2 * i + 1])

        start = 2 * len(self.free)
        for i in range(len(self.edges)):
            stride = len(self.fixed) + len(self.free)
            offset = start + stride * i
            self.edges[i] = vec[offset : offset + stride]

    # Helpers to interpret the internal data.

    def get_edge_to_free(self, i, j):
        if (i > j):
            i, j = j, i
        return self.edges[i][j + len(self.fixed)]

    def get_edge_to_fixed(self, i, fixed):
        return self.edges[i][fixed]

    def randomize(self):
        for i in range(len(self.free)):
            self.free[i] = (random.random() * 20 - 10, random.random() * 20 - 10)
        for row in self.edges:
            for j in range(len(row)):
                row[j] = random.random()

    # Helpers for humans.
    def print_desmos_copypaste(self):
        print()
        print("Paste me!!")
        print(str(self.fixed)[1:-1]) # code golfin
        print(str(self.free[:self.n_main])[1:-1])
        print(str(self.free[self.n_main:])[1:-1])
        print()
        
        # Can't paste into desmos :(
        # for i in range(len(self.free)):
        #     for j in range(len(self.free)):
        #         if (self.get_edge_to_free(i, j) < 0):
        #             continue
        #         if (self.free[i][0] >= self.free[j][0]):
        #             continue

        #         m = (self.free[i][1] - self.free[j][1]) / (self.free[i][0] - self.free[j][0])
        #         b = self.free[i][1] - m * self.free[i][0]
        #         print(f"y = {m}x + {b} {{{self.free[i][0]} < x < {self.free[j][0]}}}")

'''

if __name__ == "__main__":
    bridge = Bridge()
    print(bridge.to_vector())
    print(bridge.objective_function())
    
    print()

    bridge2 = Bridge()
    bridge2.randomize()
    bridge2.from_vector(list(range(100)))
    print(bridge2.to_vector())
    print(bridge2.objective_function())
    
    bridge2.print_desmos_copypaste()
    '''