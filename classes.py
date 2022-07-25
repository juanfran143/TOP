


class node:

    def __init__(self, id, reward, x, y):
        self.id = id
        self.reward = reward
        self.x = x
        self.y = y
        self.route = None

    def __str__(self):
        return str(self.id)

class edge:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.distance = ((start.x - end.x)**2 + (start.y - end.y)**2) ** (1/2)

    def __str__(self):
        return str(self.start.id) + " - "+str(self.end.id)

class saving():

    def __init__(self, start, end, distance, a_to_b):
        self.start = start
        self.end = end
        self.distance = distance
        self.a_to_b = a_to_b

class route:

    def __init__(self, id, edges, distancia):
        self.id = id
        self.reward = 0
        self.edges = edges
        self.distance = distancia
        self.stochastic_of = []
        self.reliability = 0

    def reverse_edges(self):
        edges = []
        for i in range(len(self.edges)):
            edges.append(edge(self.edges[-(i+1)].end, self.edges[-(i+1)].start))

        self.edges = edges

    def copy_edges(self):
        edges = []
        for i in self.edges:
            edges.append(i)

        return edges

    def __str__(self):
        text = str(self.edges[0].start) + "-"
        for i in self.edges[:-1]:
            text += str(i.end) + "-"
        text += str(self.edges[-1].end)
        return text
