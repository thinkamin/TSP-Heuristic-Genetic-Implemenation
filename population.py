class Population(object):
    def __init__(self, cities):
        self.routes = []
        self.cities = cities
    def addRoute(self,r):
        self.routes.append(r)
    # randomly generates the order of routes for generation 0
    def generateRandomRoutes(self):
        for x in range(len(self.routes)):
            b = self.cities[:]
            b = self.shuffle(b)
            self.routes[x].order = b
    # randomly shuffle a list. Processing does not offer this function natively even though it's offered by Python
    def shuffle(self,l):
        d = []
        for x in range(len(l)):
            r = int(random(len(l)))
            d.append(l[r])
            del l[r]
        return d
            
            