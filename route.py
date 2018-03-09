class Route(object):
    def __init__(self, order):
        if order is not None:
            self.order = order
        else:
            self.order = []
            pass
    # takes in two route objects (usage: route1.crossover(route2)) and returns an order which is the crossover of the two routes. 
    # this particular crossover function keeps the order and index of the cities that the routes agree on, and 
    # shuffles the indexes of the rest
    def crossover(self,mate):
        newOrder = []
        a = self.order[:]
        b = mate.order[:]
        for x in range(len(a)):
            newOrder.append([])
        for x in range(len(a)):
            if a[x] == b[x]:
                newOrder[x] = a[x]
        citiesLeft = []
        for x in range(len(newOrder)):
            if newOrder[x] == []:
                if a[x] not in citiesLeft:
                    citiesLeft.append(a[x])
                if b[x] not in citiesLeft:
                    citiesLeft.append(b[x])
        citiesLeft = self.shuffle(citiesLeft)
        for x in range(len(newOrder)):
            if newOrder[x] == []:
                newOrder[x] = citiesLeft[0]
                del citiesLeft[0]
        return newOrder
    # randomly shuffle a list. Processing does not offer this function natively even though it's offered by Python
    def shuffle(self,l):
        d = []
        for x in range(len(l)):
            r = int(random(len(l)))
            d.append(l[r])
            del l[r]
        return d
        
        