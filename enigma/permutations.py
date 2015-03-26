from itertools import permutations, product

rotors = [0,1,2,3,4]
rotorSetups = permutations(rotors, 3)
for setup in rotorSetups:
    print("{", setup[0], ",", setup[1], ",", setup[2], "},", end="", sep="")
print()
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotorSettings = product(alphabet, repeat=3)
for setting in rotorSettings:
    print("\"", setting[0], setting[1], setting[2], "\",", end="", sep="")
