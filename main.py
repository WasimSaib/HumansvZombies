from GameWorld import World
import os

# insert number of agents
humns = int(input("insert number of humans"))
zombies = int(input("insert number of zombies"))
os.system("cls")
gw = World(10, 10, humns, zombies)
gw.simulateGame()

