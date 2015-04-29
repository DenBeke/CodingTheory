"""
Convert given integer to a string
"""
def toText(value):
  asciiText = str(value)
  digrams = [asciiText[i:i+2] for i in range(0, len(asciiText), 2)]
  result = ""
  seemsGood = False
  weirdStuff = False
  ctr = 0
  for digram in digrams:
    ctr += 1
    asciiValue = int(digram)+32
    if asciiValue == 32:
      if ctr < len(asciiText)/2 - 1:
        seemsGood = True
    if asciiValue >= 127:
      return


    if not asciiValue == 32 and not (65 < asciiValue < 91) and not (96 < asciiValue < 123):
      if weirdStuff:
        return
      weirdStuff = True


    result += chr(asciiValue)
  if seemsGood:
    print(result, value)

a = 29118405404220459917506399212097843017814710983140
b = 42146349908839709291089275597341571419432358218840
p = 97067553992624667459897809313680908020593207653741

usedLetter = b
#b += 500000000 * (p-1)
#b += 330000000 * (p-1)

#for i in range(100000000):
counter = 0
stepCounter = 0
while(True):
  tostr = str(usedLetter)
  if len(tostr) % 2 or int(tostr[0:2]) > 58:
    diff = 10 ** (len(tostr)) - usedLetter
    timesp = (diff // (p-1)) + 1
    usedLetter += timesp * (p-1)
    counter += timesp
    tostr = str(usedLetter)
    
  if int(tostr[0:2]) < 33:
    diff = 33*(10**(len(tostr)-2)) - usedLetter
    timesp = (diff // (p-1)) + 1
    usedLetter += timesp * (p-1)
    counter += timesp
  toText(usedLetter)
  usedLetter += (p-1)
  counter += 1
  stepCounter += 1
  if not (stepCounter % 10000000):
    print(counter)
