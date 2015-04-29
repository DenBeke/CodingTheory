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
    #if asciiValue == 33 or asciiValue == 35 or asciiValue == 36 or asciiValue == 37 or asciiValue == 40 or asciiValue == 41 or asciiValue == 42 or asciiValue == 43 or asciiValue == 47 or asciiValue == 59 or asciiValue == 60 or asciiValue == 61 or asciiValue == 62 or asciiValue == 64 or asciiValue == 91 or asciiValue == 92 or asciiValue == 93 or asciiValue == 94 or asciiValue == 95 or asciiValue == 96 or asciiValue == 123 or asciiValue == 124 or asciiValue == 125 or asciiValue == 129:
    #  if weirdStuff:
    #    return
    #  weirdStuff = True

    if not asciiValue == 32 and not (65 < asciiValue < 91) and not (96 < asciiValue < 123):
      if weirdStuff:
        return
      weirdStuff = True


    result += chr(asciiValue)
  if seemsGood:
    print(result)

a = 29118405404220459917506399212097843017814710983140
b = 42146349908839709291089275597341571419432358218840
p = 97067553992624667459897809313680908020593207653741


counter = 0
for j in range(500000000):
  toText(a)
  a += (p-1)
  counter += 1
  if not (counter % 10000000):
    print(counter)
