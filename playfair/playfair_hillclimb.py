import random, time

"""
Try to find the best possible square, using the hillclimb technique:
first generate a couple (100) of random squares
keep 5 best. and breed these.

Best: those with the highest IC in the text
breed: create random permutations of these 5 squares
"""
def hillClimb(text):
    ALPHABET= []
    for i in range(65, 91):
        ALPHABET.append(str(chr(i)))
    
    squares = []    
    # creare random permutations:
    random1 = ALPHABET
    random2 = ALPHABET
    random.shuffle(random1, random.random)
    time.sleep(1)
    random.shuffle(random2, random.random)
    
    print (random1)
    print (random2)
    workingAlph = ALPHABET
    for i in range(0,100):
        print(random.random())
        random.shuffle(workingAlph, random.random)
        squares.append(workingAlph)
        time.sleep(0.01)
    print(squares)
    
hillClimb("AD")
