import random
import math

def distance(point, other):
    dx = point[0] - other[0]
    dy = point[1] - other[1]
    return math.sqrt(dx * dx + dy * dy)

class Bridge:
    def __init__(self, left = (-10, 0), right = (10, 0), n_main = 1, n_other = 2):
        # index 0 is always fixed, 1 is always a horizontal roller.
        # the next n_main have extra weight.
        # the rest (n_other) have some weight.
        self.nodes = [left, right]
        self.nodes.extend((i, i) for i in range(n_main + n_other))

        # Create (2 * #nodes - 3) members.
        # This makes the bridge solvable.
        self.members = [] 

        # Connect the left to the main,
        # the main to each other,
        # the main to the right
        self.members.append((0, 2))
        for i in range(n_main-1):
            self.members.append((2 + i, 2 + i + 1))
        self.members.append((2 + n_main - 1, 1))

        # repeat for the other nodes.
        start = n_main + 2
        self.members.append((0, start))
        for i in range(n_other - 1):
            self.members.append((start + i, start + i + 1))
        self.members.append((start + n_other - 1, 1))

        # now we have a big polygon!
        # connect the rest, somehow.
        # (many ways to do this, its kinda hard tbh.)
        # (TODO: make symmetrical for shenanigans)
        if n_other > n_main:
            last_main_index = 0 # 0 start intentional
            for i in range(n_other):
                main_index = (i * n_main) // n_other
                other_index = i
                self.members.append((main_index + 2, other_index + (2 + n_main)))
                if last_main_index != main_index:
                    self.members.append((main_index + 2, other_index + (2 + n_main) - 1))
                    last_main_index = main_index
        else:
            last_other_index = 0 # 0 start intentional
            for i in range(n_main):
                main_index = i
                other_index = (i * n_other) // n_main
                self.members.append((main_index + 2, other_index + (2 + n_main)))
                if last_other_index != main_index:
                    self.members.append((main_index + 2 - 1, other_index + (2 + n_main)))
                    last_other_index = other_index

        self.edge_width = [1 for i in self.members]

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

    def objective_strut_cost(self):
        return 0

    def objective_road_cost(self):
        return 0

    def equality_constraints(self):
        return []

    def inequality_constraints(self):
        constraints = self.inequality_max_stress()
        constraints.extend(self.inequality_min_length())        
        return constraints

    def inequality_max_stress(self):
        constraints = []
        
        solved = [False for vertex in self.free]
        frontier = [vertex == 0 for vertex in self.free]
        tension = [None for vertex in self.edges] # negative for tension, positive for compression

        # while any(frontier):
        #     current = frontier.index(True)
        #     sum_forces = [0, -2]            
        
        # if not all(solved):
        #     print("oh no!")
        
        return constraints

    def inequality_min_length(self):
        min_length = 0.1
        constraints = []
        for i in range(len(self.free)):
            for j in range(i, len(self.free)):
                constraints.insert(distance(self.free[i], self.free[j]) - min_length)
            for j in range(len(self.fixed)):
                constraints.insert(distance(self.free[i], self.fixed[j]) - min_length)
        return constraints

    # Vector Conversion

    def to_vector(self):
        vec = []
        for point in self.nodes[2:]:
            vec.extend(point)
        vec.extend(self.edge_width)
        return vec
    
    def from_vector(self, vec):
        for i in range(len(self.nodes) - 2):
            self.nodes[2 + i] = (vec[2 * i], vec[2 * i + 1])

        start = 2 * (len(self.nodes) - 2)
        self.edge_width = vec[start : start + len(self.edge_width)]

    # Helpers to interpret the internal data.
    def randomize(self):
        for i in range(len(self.free)):
            self.free[i] = (random.random() * 20 - 10, random.random() * 20 - 10)
        for row in self.edges:
            for j in range(len(row)):
                row[j] = random.random()

    # Helpers for humans.
    # def print_desmos_copypaste(self):
    #     print()
    #     print("Paste me!!")
    #     print(str(self.fixed)[1:-1]) # code golfin
    #     print(str(self.free[:self.n_main])[1:-1])
    #     print(str(self.free[self.n_main:])[1:-1])
    #     print()
        
    #     # Can't paste into desmos :(
    #     for i in range(len(self.free)):
    #         for j in range(len(self.free)):
    #             if (self.get_edge_to_free(i, j) < 0):
    #                 continue
    #             if (self.free[i][0] >= self.free[j][0]):
    #                 continue

    #             m = (self.free[i][1] - self.free[j][1]) / (self.free[i][0] - self.free[j][0])
    #             b = self.free[i][1] - m * self.free[i][0]
    #             print(f"y = {m}x + {b}") # {{{self.free[i][0]} < x < {self.free[j][0]}}}")

if __name__ == "__main__":
    for main in range(1, 10):
        for other in range(1, 10):
            aaaa = Bridge()
            assert(len(aaaa.members) + 3 == 2 * len(aaaa.nodes))

    # Manual sanity checks
    bridge = Bridge()
    print("  Nodes:", str(bridge.nodes))
    print("Members:", str(bridge.members))

    print(" Vector:", bridge.to_vector())
    print("Objctve:", bridge.objective_function())

    bridge2 = Bridge()
    # bridge2.randomize()
    bridge2.from_vector(list(range(100)))
    print(bridge2.to_vector())
    # print(bridge2.objective_function())
    
    # bridge2.print_desmos_copypaste()