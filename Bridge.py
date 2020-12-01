class Bridge:
    def __init__(self, n_fixed = 2, n_main = 3, n_free = 3):

        # probably could be renamed :)
        self.main = [(0, 0) for i in range(n_main)]
        self.free = [(0, 0) for i in range(n_free)]
        
        # [free] x [free U main U fixed]
        self.edges = [[0 for j in range(n_fixed + n_main + n_free)] for i in range(n_free)]

        # TODO: theres some wasted space, edge[i][j] means the same as edge[j][i]
        # and edge[i][i] is useless
        # we'll ignore it for now :)

    def to_vector(self):
        vec = []
        for point in self.main:
            vec.extend(point)
        for point in self.free:
            vec.extend(point)
        for row in self.edges:
            vec.extend(row)
        return vec
    
    def from_vector(self, vec):
        # TODO: someone else get this lmao
        pass

    def get_edge_to_free(self, i, j):
        if (i > j):
            i, j = j, i
        return self.edges[i][j]
    
    def get_edge_to_main(self, i, main):
        return self.edges[i][main + len(self.free)]

    def get_edge_to_fixed(self, i, fixed):
        return self.edges[i][fixed + len(self.free) + len(self.main)]

if __name__ == "__main__":
    bridge = Bridge()
    print(bridge.to_vector())