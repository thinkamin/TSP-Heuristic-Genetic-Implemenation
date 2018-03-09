# Designed and Written by Kyle Thorpe, 2018
# Uses a genetic algorithm to find a local minimum solution to the travelling salesman problem

from population import Population
from route import Route

# the dimensions of the screen to display
width = 1280
height = 1280
# how much space between the edge of the screen and a possible city being randomly placed there
border = 40
# amount of cities to randomly generate
cities = 15
# a list containing lists. each list is indexed as [x,y,id] where x and y are the coordinates and id is the id of the city
cities_pos = []
# the current population of routes. intitialized in setup()
population = None
# how many routes per generation
populationSize = 100
# the shortest length of the previous generation, used for calculating the last error
prevSL = 0
# the current generation number
generation = 0
# how often a mutation happens. between 0.0 and 1.0
mutationRate = 0.03
# the last error - calculated as errorTerm = prevSL - shortestLength
errorTerm = 0
def setup():
    global population
    # set the background of the screen to black
    background(0)
    strokeWeight(1)
    # set the size of the screen to display
    size(width, height)
    # randomly generate cities within the bounds of the screen within the border
    for i in range(cities):
        cities_pos.append([random(border,width-border),random(border,height-border),i])
    # create the population object. this stores the current routes and the cities
    population = Population(cities_pos)
    # add blank routes to the population object
    for i in range(populationSize):
        r = Route(None)
        population.addRoute(r)
    # randomly assign an order to each route
    population.generateRandomRoutes()
        
        
def draw():
    global generation
    global prevSL
    background(0)
    # clear all previous drawings on the window
    clear()
    # draw the cities as a circle
    for x in cities_pos:
        fill(255,255,255)
        ellipse(x[0],x[1], 10, 10)
    lengthRoutes = []
    linesToDraw = []
    # calculate all of the lines to draw from each of the routes. these lines connect the cities. add the lines to draw to linesToDraw[]
    for i in range(len(population.routes)):
        order = population.routes[i].order
        length = 0
        for x in range(len(order)-1):
            currX = order[x][0]
            currY = order[x][1]
            nextX = order[x+1][0]
            nextY = order[x+1][1]
            l = [currX,currY,nextX,nextY]
            linesToDraw.append(l)
            length += calcDistance(order[x],order[x+1])
        lengthRoutes.append(length)
    # find best (shortest) route and draw it (green)
    shortestLength = float("inf")
    shortestIndex = -1
    for x in range(len(lengthRoutes)):
        if lengthRoutes[x] < shortestLength:
            shortestIndex = x
            shortestLength = lengthRoutes[x]
    # calculate the error term
    shortestRoute = population.routes[shortestIndex].order
    errorTerm = prevSL - shortestLength
    # if the error term has changed substantitally (meaning the generations are still changing quite a lot) then draw all of the lines on every route
    if(abs(errorTerm)>500):
        stroke(255,255,255)
        strokeWeight(1)
        for x in linesToDraw:
            # I have commented out the drawing of non-shortest routes to speed up run time
            #line(x[0],x[1],x[2],x[3])
            pass
    # set the previous shortest length to the current one
    prevSL = shortestLength
    
    # color the start and end cities of the shortest route RED
    for x in range(len(shortestRoute)-1):
        currX = shortestRoute[x][0]
        currY = shortestRoute[x][1]
        nextX = shortestRoute[x+1][0]
        nextY = shortestRoute[x+1][1]
        stroke(0,255,29)
        strokeWeight(4)
        line(currX,currY,nextX,nextY)
        if x == 0:
            fill(255,0,0)
            ellipse(currX,currY,20,20)
        if x == len(shortestRoute)-2:
            fill(255,0,0)
            ellipse(nextX,nextY,20,20)
    print(shortestLength)
    # calculate the fitness of all of the routes. gives a value between 0.0 and 1.0
    fitness = []
    for x in lengthRoutes:
        x = 1/(x/shortestLength)
        fitness.append(pow(x,15))
    fitnessTotal = sum(fitness)
    chances = []
    # assigns every route in the current population a chance at reproducing between 0.0 and 1.0
    for x in fitness:
        chances.append(x/fitnessTotal)
    j = 0
    genePool = []
    # assigns every route in the current population a range. consists of L and H where 0.0 <= L < H <= 1.0
    for x in chances:
        genePool.append([j,j+x])
        j+=x
    # print out information about the current generation and the total lifespan
    s = "Generation "+str(generation)+"\nLast Error "+str(errorTerm)
    textSize(32)
    text(s,20,height-60)
    s = "Mutation Rate "+str(mutationRate)+"\nGeneration Size "+str(populationSize)+"\nCities "+str(cities)
    text(s,20,40)
    P = Population(cities_pos)
    selection(P,genePool)
# select randomly from the genePool of probability ranges 2 routes. then cross the 'DNA' from each route over to create a new route
def selection(P,genePool):
    for i in range(populationSize):
        parents = selectParents(genePool)
        a = population.routes[parents[0]]
        b = population.routes[parents[1]]
        newOrder = a.crossover(b)
        newRoute = Route(newOrder)
        newRoute = mutate(newRoute)
        P.addRoute(newRoute)
    newGeneration(P)
# reset variables for new generation
def newGeneration(P):
    global generation
    global population
    population = P
    generation += 1
# based on the mutationRate, if a route which is passed into mutate(route) is selected randomly, then swap two cities in the order of the route
def mutate(route):
    nr = route.order[:]
    for x in range(len(nr)):
        chance = random(0.0,1.0)
        if(chance < mutationRate):
            rand1 = int(random(len(nr)))
            rand2 = int(random(len(nr)))
            temp = nr[rand1]
            nr[rand1] = nr[rand2]
            nr[rand2] = temp
    return Route(nr)
#returns two indexes of two parents chosen randomly out of the genePool list of chance ranges
def selectParents(genePool):
    a = None
    b = None
    while a is None or b is None or a == b:
        aChance = random(0.0,1.0)
        bChance = random(0.0,1.0)
        for x in range(len(genePool)):
            if (a is None or a == b) and aChance >= genePool[x][0] and aChance < genePool[x][1]:
                a = x
            if (b is None or b == a) and aChance >= genePool[x][0] and aChance < genePool[x][1]:
                b = x
    if a is None or b is None:
        print("fatal error. no parents selected")
    return [a,b]
        
        
    
    
    
def getPathDistance(path):
    totalDistance = 0
    for x in range(len(path)-1):
        totalDistance += calcDistance(path[x],path[x+1])
    return totalDistance
        
def calcDistance(a,b):
    d = pow((a[0] - b[0]),2)
    d = d + pow((a[1] - b[1]),2)
    d = sqrt(d)
    return d