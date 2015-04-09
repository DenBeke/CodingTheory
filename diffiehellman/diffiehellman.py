import math

"""
returns g^u mod n
"""
def powermod(g, u, n):
    binaryExp = 1
    outcomes = {1: g % n}
    solution = 1
    while binaryExp <= u:
        newBinaryExp = binaryExp * 2
        outcomes[newBinaryExp] = (outcomes[binaryExp]**2) % n
        binaryExp = newBinaryExp
    while binaryExp >=1:
        if binaryExp <= u:
            solution *= outcomes[binaryExp]
            solution %= n
            if binaryExp == u:
                break #solution reached, no need to go on
            u -= binaryExp
        binaryExp //= 2
    return solution


"""
For q a prime factor of p-1, appearing count times in its prime factorization,
find an xi as defined by the Pohlig-Hellman Algorithm
"""
def pohligHellmanStep(beta, alpha, p, q, count):
  x = 0
  powerQ = q
  for i in range(count):
    left = powermod(beta, (p-1)//powerQ, p)
    for thisX in range(q):
      if powermod(alpha, ((p-1)//q)*thisX, p) == left:
        prevX = thisX
        break
    exponent = ((q**i) * -prevX) % (p-1)
    beta = beta * powermod(alpha, exponent, p)
    powerQ *= q
    x += prevX * (q**i)
    x %= (q**count)
  print("Prime", q, "gets x", x)


"""
Same as above, but starts with highest possible xi
"""
def pohligHellmanReverse(beta, alpha, p, q, count):
  x = 0
  powerQ = q
  for i in range(count):
    left = powermod(beta, (p-1)//powerQ, p)
    for thisX in range(q, -1, -1):
      if powermod(alpha, ((p-1)//q)*thisX, p) == left:
        prevX = thisX
        break
    exponent = ((q**i) * -prevX) % (p-1)
    beta = beta * powermod(alpha, exponent, p)
    powerQ *= q
    x += prevX * (q**i)
    x %= (q**count)
  print("Prime", q, "gets x", x)

"""
Extended euclidian algorithm, finds s and t
such that sa * tb = gcd(a,b) if a > b or else sb * ta = gcd(a,b)
"""
def euclidianAlgo(a, b):
  r0 = max(a,b)
  r1 = min(a,b)
  t0 = 1
  t1 = 0
  s0 = 0
  s1 = 1
  
  while r1 != 0:
    q1 = r0 // r1
    r2 = r0 % r1
    t2 = -q1*t1 + t0
    s2 = -q1*s1 + s0
    
    t0 = t1
    t1 = t2
    s0 = s1
    s1 = s2
    r0 = r1
    r1 = r2

  return (t0, s0)

"""
Finds x through chinese remainder theorem, from data provided as a list of pairs
containing the modulus (divisor of p-1) followed by the xi
"""
def chineseRemainder(stepResults):
  p = 1
  for pair in stepResults:
    p *= pair[0]
  p += 1
  result = 0
  for i in range(len(stepResults)):
    a = 1
    b = stepResults[i][0]
    for j in range(len(stepResults)):
      if i == j:
        continue
      a *= stepResults[j][0]
    (s,t) = euclidianAlgo(a,b)
    if a > b:
      result += stepResults[i][1] * s * a
    else:
      result += stepResults[i][1] * t * a
    result %= p-1
  return result

"""
Convert given integer to a string
"""
def toText(value):
  asciiText = str(value)
  digrams = [asciiText[i:i+2] for i in range(0, len(asciiText), 2)]
  result = ""
  for digram in digrams:
    asciiValue = int(digram)+32
    result += chr(asciiValue)
  print(result)

p = 97067553992624667459897809313680908020593207653741
g = 8754324567890876543245678908765432456789

A = 93965208631426420710108237044685554466463776793445
B = 29568451090985766529117441313265572634102365023888

      
#use this to get the xi (takes a LONG time)
#primes = [(2,2), (3,2), (5,1), (19,1), (71,2), (79,1), (1471,1), (14087,1), (70379,1), (9110581,1), (9126043,1), (9726001,1), (60432007,1)]
#for prime in primes:
#  pohligHellmanStep(A, g, p, prime[0], prime[1])
#  pohligHellmanStep(B, g, p, prime[0], prime[1])


#use this to get a or b, through values determined above
#print(chineseRemainder([(2**2,0), (3**2,1), (5,0), (19,15), (71**2, 1504), (79, 0), (1471, 327), (14087, 5649), (70379, 53990), (9110581, 1621858), (9126043, 7487110), (9726001, 5962660), (60432007, 44789738)]))
#print(chineseRemainder([(2**2,0), (3**2,8), (5,0), (19,18), (71**2, 1874), (79, 0), (1471, 1214), (14087, 8542), (70379, 41725), (9110581, 5918548), (9126043, 4368382), (9726001, 2344520), (60432007, 3374968)]))


a = 29118405404220459917506399212097843017814710983140
b = 42146349908839709291089275597341571419432358218840
sharedKey = 76755567381519549143666616401510211097526907381540

#Verify correctness of results
print(powermod(g, a, p) == A)
print(powermod(g, b, p) == B)
print(powermod(B, a, p) == powermod(A, b, p))
