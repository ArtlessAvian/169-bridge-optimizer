from Bridge import Bridge
import math 

class Problem:
    def __init__(self, bridge = Bridge()):
        self.bridge = bridge

    # def get_dimension(self):
        # return len(self.bridge.to_vector())

    def objective_function(self, vec):
        self.bridge.from_vector(vec)
        return self.bridge.objective_function()
    
    def equality_constraints(self, vec):
        self.bridge.from_vector(vec)
        return self.bridge.equality_constraints()

    def inequality_constraints(self, vec):
        self.bridge.from_vector(vec)
        return self.bridge.inequality_constraints()

'''
if __name__ == "__main__":
    
    # Example usage?
    bridge = Bridge()
    bridge.randomize()
    print(bridge.objective_function())
    bridge.print_desmos_copypaste()

    problem = Problem(bridge)
    vec = bridge.to_vector()

    for i in range(100):
        grad = calculate_gradient(vec, problem.objective_function)
        # print(grad)
        vec = [vec[i] - grad[i] / 100 for i in range(len(vec))]
        # print(vec)

    # print([round(i*1000) / 1000 for i in vec])
    bridge.from_vector(vec)
    bridge.print_desmos_copypaste()
    print(bridge.objective_function())
'''