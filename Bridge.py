import random
import math

def distance(point, other):
    dx = point[0] - other[0]
    dy = point[1] - other[1]
    return math.sqrt(dx * dx + dy * dy)

class Bridge:
    def __init__(self, n_main = 1, n_other = 1, left = (-10, 0), right = (10, 0)):
        # index 0 is always fixed, 1 is always a horizontal roller.
        # the next n_main have extra weight.
        # the rest (n_other) have some weight.
        self.nodes = [left, right]
        self.nodes.extend((i, 0) for i in range(n_main))
        self.nodes.extend((i, 5) for i in range(n_other))

        self.n_main = n_main

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
                if last_other_index != other_index:
                    self.members.append((main_index + 2 - 1, other_index + (2 + n_main)))
                    last_other_index = other_index

        self.edge_width = [1 for i in self.members]

        self.road_cost_per_length = 10

    def objective_function(self):
        return self.objective_strut_cost() + self.objective_road_cost()

    def objective_strut_cost(self):
        cost = 0
        for member, width in zip(self.members, self.edge_width):
            dist = distance(self.nodes[member[0]], self.nodes[member[1]])
            cost += dist * max(0, width)
        return cost

    # Encourages the main road to be straight.
    def objective_road_cost(self):
        road_length = distance(self.nodes[0], self.nodes[2])
        for i in range(self.n_main - 1):
            road_length += distance(self.nodes[2 + i], self.nodes[2 + i + 1])
        road_length += distance(self.nodes[self.n_main + 1], self.nodes[1])

        return road_length * self.road_cost_per_length

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
        self.edge_width = [abs(i) for i in vec[start : start + len(self.edge_width)]]

    # Helpers to interpret the internal data.
    def randomize(self):
        for i in range(2,len(self.nodes)):
            self.nodes[i] = (random.random() * 20 - 10, random.random() * 20 - 10)
        for i in range(len(self.edge_width)):
            self.edge_width[i] = random.random()

    # Helpers for humans.
    def print_desmos_copypaste(self):
        print()
        print("Paste me into Desmos!!!")
        print(str(self.nodes[:2])[1:-1]) # code golfin
        print(str(self.nodes[2:self.n_main+2])[1:-1])
        print(str(self.nodes[self.n_main+2:])[1:-1])
        
        for a, b in self.members:
            dx = self.nodes[b][0] - self.nodes[a][0]
            dy = self.nodes[b][1] - self.nodes[a][1]
            x = self.nodes[a][0]
            y = self.nodes[a][1]
            print(f"({dx:.5f}t + {x:.5f}, {dy:.5f}t + {y:.5f})")
        print()

if __name__ == "__main__":
    # Test if always statically determinate
    for main in range(1, 20):
        for other in range(1, 20):
            determ = Bridge(main, other)
            assert(len(determ.members) + 3 == 2 * len(determ.nodes))

    # Test that vectors work as intended
    bridge_vec = Bridge(10,10)
    bridge_vec.from_vector(list(range(1000)))
    vec = bridge_vec.to_vector()
    for i, j in zip(vec, vec[1:]):
        assert(i+1 == j)

    # Manual sanity checks
    bridge = Bridge(1, 5)
    print("  Nodes:", str(bridge.nodes))
    print("Members:", str(bridge.members))

    print(" Vector:", bridge.to_vector())
    print("Objctve:", bridge.objective_function())

    bridge.print_desmos_copypaste()