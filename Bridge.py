import random
import math
from numpy import linalg
import numpy as np


def distance(point, other):
    return math.sqrt(np.dot(point - other, point - other))

def normalizedDiff(to, fromm):
    dist = distance(to, fromm)
    if dist == 0:
        return (0, 1) # tbh, idk
    return (to - fromm) / dist

class Bridge:
    def __init__(self, n_main = 1, n_other = 1, left = (-10, 0), right = (10, 0)):
        # index 0 is always fixed, 1 is always a horizontal roller.
        # the next n_main have extra weight.
        # the rest (n_other) have some weight.
        self.nodes = [left, right]
        self.nodes.extend((((i + 1) / (n_main + 1)) * 20 - 10, 0) for i in range(n_main))
        self.nodes.extend((((i + 1) / (n_other + 1)) * 20 - 10, 5) for i in range(n_other))
        self.nodes = np.array(self.nodes)

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

        # self.edge_width = np.ones(len(self.members))
        # self.force_interior()

        self.coeff = None

        self.road_cost_per_length = 100

    def objective_function(self):
        return self.objective_strut_cost() + self.objective_road_cost()

    def objective_strut_cost(self):
        cost = 0
        for member, width in zip(self.members, self.get_tensions()):
            dist = distance(self.nodes[member[0]], self.nodes[member[1]])
            cost += dist * abs(width)
        return cost

    # Encourages the main road to be straight.
    def objective_road_cost(self):
        road_length = distance(self.nodes[0], self.nodes[2])
        for i in range(self.n_main - 1):
            road_length += distance(self.nodes[2 + i], self.nodes[2 + i + 1])
        road_length += distance(self.nodes[self.n_main + 1], self.nodes[1])

        return road_length * self.road_cost_per_length

    def inequality_constraints(self):
        return self.inequality_min_length()
        # self.inequality_max_stress()

    def coeff_matrix(self, force_recalc = False):
        coeff = np.zeros((2 * len(self.nodes), len(self.members) + 3))

        # internal forces
        coeff[0][len(self.members)] = 1 # pin's x
        coeff[1][len(self.members) + 1] = 1 # pin's y
        coeff[3][len(self.members) + 2] = 1 # roller's y
        # i is the compression/tension
        for i, (fromm, to) in enumerate(self.members):
            dx, dy = normalizedDiff(self.nodes[to], self.nodes[fromm])
            # solving for i
            # 0 = ... + i * dx + ...
            coeff[2*fromm][i] = dx
            # 0 = ... + i * dy + ...
            coeff[2*fromm+1][i] = dy
            # repeat
            coeff[2*to][i] = -dx
            coeff[2*to+1][i] = -dy

        return coeff

    def net_force_vector(self):
        net_forces = np.zeros(2 * len(self.nodes))
        # Push down on all main nodes
        for i in range(2, len(self.nodes)):
            net_forces[2 * i + 1] = 10 if i < self.n_main + 2 else 2
        return net_forces
    
    def get_tensions(self):
        net_forces = self.net_force_vector()
        try:
            return linalg.solve(self.coeff_matrix(), net_forces)
        except linalg.LinAlgError:
            return np.full_like(net_forces, 1e8)

    # def inequality_max_stress(self):        
    #     sumforces = np.zeros(2 * len(self.nodes))
    #     # Push down on all main nodes
    #     for i in range(2, len(self.nodes)):
    #         sumforces[2 * i + 1] = 10 if i < self.n_main + 2 else 2

    #     try:
    #         tensions = linalg.solve(self.coeff_matrix(), sumforces)
    #     except linalg.LinAlgError:
    #         return np.full_like(sumforces, -1e8)

    #     constraints = self.edge_width - np.absolute(tensions[:len(self.edge_width)])
    #     return constraints

    min_length = 0.5
    def inequality_min_length(self):
        distances = []
        for i, j in self.members:
            distances.append(distance(self.nodes[i], self.nodes[j]))
        return np.array(distances) - Bridge.min_length

    # Vector Conversion

    def to_vector(self):
        vec = []
        for point in self.nodes[2:]:
            vec.extend(point)
        # vec.extend(self.edge_width)
        return np.array(vec)

    def from_vector(self, vec):
        nodes_slice = vec[: 2 * (len(self.nodes)-2)].reshape((len(self.nodes)-2, 2))
        self.nodes = np.append(self.nodes[:2], nodes_slice, 0)

        # start = 2 * (len(self.nodes) - 2)
        # self.edge_width = np.absolute(vec[start : start + len(self.edge_width)])

    # Helpers to interpret the internal data.
    def randomize(self):
        for i in range(2,len(self.nodes)):
            self.nodes[i] = (random.random() * 20 - 10, random.random() * 20 - 10)

        # self.force_interior()

    # def force_interior(self):
        # for power in range(20):
        #     for i in range(len(self.edge_width)):
        #         self.edge_width[i] = 2 ** power
        #     if all(i > 0 for i in self.inequality_max_stress()):
        #         break

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
    # for main in range(1, 20):
    #     for other in range(1, 20):
    #         determ = Bridge(main, other)
    #         assert(len(determ.members) + 3 == 2 * len(determ.nodes))

    # Test if solvable on init
    # for main in range(1, 20):
    #     for other in range(1, 20):
    #         inverse = Bridge(main, other)
    #         inverse.randomize()
    #         linalg.inv(inverse.coeff_matrix())

    # Test that vectors work as intended
    # bridge_vec = Bridge(10,10)
    # bridge_vec.from_vector(list(range(1000)))
    # vec = bridge_vec.to_vector()
    # for i, j in zip(vec, vec[1:]):
    #     assert(i+1 == j)

    # Manual sanity checks
    bridge = Bridge(3, 2)
    # bridge.randomize()

    print("Nodes:")
    print(str(bridge.nodes))
    print("\nMembers:")
    print(str(bridge.members))

    print("\nAs Vector:")
    print(bridge.to_vector())
    print("\nObjctve:")
    print(bridge.objective_function())

    # print("\nExtra Stress:")
    # print(bridge.inequality_max_stress())
    # print("\nSolvable?:")
    # print(all(i > 0 for i in bridge.inequality_max_stress()))

    print("\nExtra Distances:")
    print(bridge.inequality_min_length())
    print("\nSolvable?:")
    print(all(i > 0 for i in bridge.inequality_min_length()))

    # print(bridge.inequality_constraints())

    # bridge.print_desmos_copypaste()
