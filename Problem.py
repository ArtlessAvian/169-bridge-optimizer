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

class ConjugateGradientDescent:
    def __init__(self, grad):
        self.gradient = grad
        self.direction = NormalizeVector(self.gradient)

    def step(self, func, vec):
        newGradient = calculate_gradient(vec, func)
        beta = max(0, DotProduct(newGradient, SubtractVectors(newGradient, self.gradient)) / DotProduct(self.gradient, self.gradient))
        newDirection = NormalizeVector(newGradient)
        newVec = line_search(func, vec, newDirection)
        self.gradient = newGradient
        self.direction = newDirection
        return newVec

    

def VectorMagnitude(vec1):
    magnitude = 0
    for i in range(len(vec1)):
        magnitude += vec1[i] * vec1[i]
    return math.sqrt(magnitude)

def NormalizeVector(vec1):
    magnitude = VectorMagnitude(vec1)
    for i in range(len(vec1)):
        vec1[i] /= magnitude * -1
    return vec1

def SubtractVectors(vec1, vec2):
    result = []
    for i in range(len(vec1)):
        result.append(vec1[i] - vec2[i])
    return result

def AddVectors(vec1, vec2):
        result = []
    for i in range(len(vec1)):
        result.append(vec1[i] + vec2[i])
    return result



def DotProduct(vec1, vec2):
    #assume vec1 and vec2 have equal lengths
    dot = 0
    for i in range(len(vec1)):
        dot += vec1[i] * vec2[i]
    return dot



# Move to optimizer!
def calculate_gradient(vec, func, small_step = 1e-8):
    gradient = []
    old = func(vec)
    for i in range(len(vec)):
        vec[i] += small_step
        new = func(vec)
        vec[i] -= small_step
        vec[i] -= small_step
        old = func(vec)
        vec[i] += small_step
        
        partial = (new - old) / small_step # / 2
        gradient.append(partial)    
    return gradient

def line_search(func, vec, direction):
    objective = lambda a: func()




if __name__ == "__main__":
    
    # Example usage?
    bridge = Bridge()
    bridge.randomize()
    print(bridge.objective_function())
    bridge.print_desmos_copypaste()
    vec = [1, 2, 3, 4]
    print(f"Hello {VectorMagnitude(vec)}")
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