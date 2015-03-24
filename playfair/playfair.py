from collections import Counter, OrderedDict
from itertools import combinations, permutations, groupby
from random import randint, seed
import os

"""
This is the row-major representation of a matrix containing the logarithms of the frequencies of digrams in English literature.
They have been rescaled to 0-9.
First character of the digram is the row, second character is the column, both in alphabetical order.
Note that J is included here!
"""
DigramFreqs = "4787467573687937398967657474208111630721710653712060825273287276218226476130407656865584366575367765606297888766745879775998577673745376447226538407576240507554755773265575276663505185449434831554842657625050758777744258797647884735055000400030000050000060000054327424622436531365304050855785448258548524666550718643842471046476136561406086788696846656853589656362667768666367897739789684537333732672173276076660304000000000000000000000600000866796658366668636886560718676865784666687458974706286658659833665962788747072667664646237785608883343436100800070000050001021003073347328722446730555214031414242035101103501252022306666665563356586357643624240005000300200300010200044"


"""
Pick one of these numbers at random during the Churn algorithm. If the difference between the parent key and the child key is less than the chosen number, 
replace the parent key with the child key to get out of local maximums.
These numbers were calculated by analysing results of simulated annealing.
"""
churnNumbers=[1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3,
4,4,4,4,5,5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,
8,8,9,9,9,9,10,10,10,10,10,11,11,11,11,
12,12,12,12,13,13,14,14,15,15,16,16,16,
16,17,17,18,18,19,19,20,21,21,22,23,23,
24,25,26,27,28,29,30,31,33,34,37,39,41,43,48,57,60]

"""
Both the digram frequencies and the churn numbers were found on http://www.cryptoden.com/
where they were provided for people attempting to solve ciphers
"""


"""
Get reverse Playfair mapping for decoding
"""
def getDigram(code, key):
  codeLeftIndex = key.index(code[0])
  codeLeftRow = int(codeLeftIndex/5)
  codeLeftCol = codeLeftIndex%5

  codeRightIndex = key.index(code[1])
  codeRightRow = int(codeRightIndex/5)
  codeRightCol = codeRightIndex%5


  if codeLeftRow == codeRightRow: #same row
    plainLeftRow, plainRightRow = codeLeftRow, codeRightRow
    plainLeftCol = codeLeftCol - 1
    if plainLeftCol == -1:
      plainLeftCol = 4
    plainRightCol = codeRightCol - 1
    if plainRightCol == -1:
      plainRightCol = 4


  elif codeLeftCol == codeRightCol: #same col
    plainLeftCol, plainRightCol = codeLeftCol, codeRightCol
    plainLeftRow = codeLeftRow - 1
    if plainLeftRow == -1:
      plainLeftRow = 4
    plainRightRow = codeRightRow - 1
    if plainRightRow == -1:
      plainRightRow = 4

  else: #different row/col
    plainLeftRow = codeLeftRow
    plainLeftCol = codeRightCol
    plainRightRow = codeRightRow
    plainRightCol = codeLeftCol
  return key[plainLeftRow*5 + plainLeftCol] + key[plainRightRow*5 + plainRightCol]

"""
Reverse the order of the rows in key and return the result
"""
def verticalFlip(key):
  newKey = key[20:25] + key[15:20] + key [10:15] + key[5:10] + key[0:5]
  return newKey

"""
Reverse the order of the columns in key and return the result
"""
def horizontalFlip(key):
  newKey =  key[4::-1] + key[9:4:-1] + key[14:9:-1] + key[19:14:-1] + key[24:19:-1]
  #newKey = cols[0][0] + cols[1][0] + cols[2][0] + cols[3][0] + cols[4][0] + cols[0][1] + cols[1][1] + cols[2][1] + cols[3][1] + cols[4][1] + cols[0][2] + cols[1][2] + cols[2][2] + cols[3][2] + cols[4][2] + cols[0][3] + cols[1][3] + cols[2][3] + cols[3][3] + cols[4][3] + cols[0][4] + cols[1][4] + cols[2][4] + cols[3][4] + cols[4][4]
  return newKey

"""
Reverse the order of the rows and columns in key and return the result (==mirrors the matrix)
"""
def fullFlip(key):
  newKey = verticalFlip(horizontalFlip(key))
  return newKey

"""
Chooses two different rows at random and swaps them
"""
def randomRowSwap(key):
  rows = [key[i:i+5] for i in range(0, len(key), 5)]
  order = [0,1,2,3,4]
  row1 = randint(0,4)
  row2 = row1
  while row2 == row1:
    row2 = randint(0,4) #make sure it's not the same one
  order[row1] = row2
  order[row2] = row1
  newKey = rows[order[0]] + rows[order[1]] + rows[order[2]] + rows[order[3]] + rows[order[4]]
  return newKey

"""
Chooses two different columns at random and swaps them
"""
def randomColSwap(key):
  cols = []
  for i in range(5):
    cols.append(key[i] + key[5+i] + key[10+i] + key[15+i] + key[20+i])
  order = [0,1,2,3,4]
  col1 = randint(0,4)
  col2 = col1
  while col2 == col1:
    col2 = randint(0,4)
  order[col1] = col2
  order[col2] = col1
  newKey = cols[order[0]][0] + cols[order[1]][0] + cols[order[2]][0] + cols[order[3]][0] + cols[order[4]][0] + cols[order[0]][1] + cols[order[1]][1] + cols[order[2]][1] + cols[order[3]][1] + cols[order[4]][1] + cols[order[0]][2] + cols[order[1]][2] + cols[order[2]][2] + cols[order[3]][2] + cols[order[4]][2] + cols[order[0]][3] + cols[order[1]][3] + cols[order[2]][3] + cols[order[3]][3] + cols[order[4]][3] + cols[order[0]][4] + cols[order[1]][4] + cols[order[2]][4] + cols[order[3]][4] + cols[order[4]][4]
  return newKey


"""
Chooses two different letters at random and swaps them
"""
def randomLetterSwap(key):
  letter1 = randint(0,24)
  letter2 = letter1
  while letter2 == letter1:
    letter2 = randint(0,24)
  if (letter1 > letter2):
    letter1, letter2 = letter2, letter1 #swap
  if letter2 == 24: #prevent out-of-bounds index if final letter is getting swapped
    newKey = key[0:letter1] + key[letter2] + key[letter1 + 1:letter2] + key[letter1]
  else:
    newKey = key[0:letter1] + key[letter2] + key[letter1 + 1:letter2] + key[letter1] + key[letter2 + 1:]
  return newKey

"""
Apply one of the six above modifications to the key
Strongly prefers the randomLetterSwap
"""
def modifyKey(parentKey):
  decider = randint(1,50)
  if decider == 1:
    return verticalFlip(parentKey)
  elif decider == 2:
    return horizontalFlip(parentKey)
  elif decider == 3:
    return fullFlip(parentKey)
  elif decider == 4:
    return randomRowSwap(parentKey)
  elif decider == 5:
    return randomColSwap(parentKey)
  else: # 6 <= decider <= 50
    return randomLetterSwap(parentKey)

"""
Give the provided text a score based on the frequency of digrams, assuming it's English
"""
def digramScore(text) :
  score = 0
  #Count all digrams, not just the even ones
  digrams1 = [text[i:i+2] for i in range(0, len(text), 2)]
  text = text[1:len(text)-1] #also cut off last char to get even length 
  digrams2 = [text[i:i+2] for i in range(0, len(text), 2)]
  digrams = digrams1 + digrams2
  c = Counter(digrams) #get the frequencies
  for (digram, freq) in c.items():
    row = ord(digram[0]) - 65
    col = ord(digram[1]) - 65
    englishFreq = DigramFreqs[row*26 + col] #grab the score for this digram
    score += int(englishFreq) * freq #add score for all appearances of this digram
    #adjust for extra Xs in playfair
    #+1 for each X that might have been inserted to split up a frequent digram
    if digram[0] == 'X':
      if 4 < int(DigramFreqs[col*27]) < 8:
        score += freq
      elif 8 <= int(DigramFreqs[col*27]):
        score += 2*freq
    if digram[1] == 'X':
      if 4 < int(DigramFreqs[row*27]) < 8:
        score += freq
      elif 8 <= int(DigramFreqs[row*27]):
        score += 2*freq
  return score

"""
Decipher the given ciphertext encoded using Playfair by applying the Churn algorithm
as explained in detail at http://www.cryptoden.com/index.php/algorithms/churn-algorithm/20-churn-algorithm

"""
def churn(text):
  #Feel free to try the algorithm with a random seed by removing the first two lines of code
  #Fast runtimes not guaranteed with random seed!
  #goodSeed = b'>>#t\xe9<\x16f!\x9f$\xc8D\xad\xbb\xa6\xae\xeb\xbd\x9c'
  #seed(goodSeed)
  parentKey = "ABCDEFGHIKLMNOPQRSTUVWXYZ" #start with the alphabet as a key
  maxScore = 0
  bestKey = ""
  bestPlain = ""
  iterations = 0 #total number of iterations
  noChange = 0 #number of iterations since latest maxScore increase
  rollbacks = 0 #number of rollbacks since latest maxScore increase
  while True:
    iterations += 1
    digrams = [text[i:i+2] for i in range(0, len(text), 2)]
    parentPlain = "" 
    #get the plaintext for the parentkey and score it
    for digram in digrams:
      parentPlain += getDigram(digram, parentKey)
    parentScore = digramScore(parentPlain)

    #Keep track of how many times the score does not change
    noChange += 1
    #If no change is made for a long time with a less-than-great score, rollback or restart
    #This latestScore limit should be set manually for different ciphertexts
    if noChange == 200:
      if rollbacks >= 10 and maxScore < 20000:
        #Start over if no progress was made after 10 rollbacks, unless we're close to a solution
        parentKey = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        noChange = 0
        rollbacks = 0
        bestKey = ""
        maxScore = 0
        bestPlain = ""
        continue
      #else rollback to best key so far
      #no need to reset bestPlain as it won't be used
      parentKey = bestKey
      noChange = 0
      print("ROLLBACK")
      rollbacks += 1
      continue


    #store best score along with used key and generated plaintext
    if parentScore > maxScore:
      rollbacks = 0
      noChange = 0
      maxScore = parentScore
      bestKey = parentKey
      bestPlain = parentPlain

      print("Iteration ", iterations, ": ", maxScore, bestKey, bestPlain, "\n")

    #This will make sure the algorithm ends once finding the correct plaintext
    #This value can only be set after deciphering once, remove this if plaintext is still not known
    if maxScore == 21055:
      return 0

    #Randomly modify parentKey to get a new key
    childKey = modifyKey(parentKey)
    childPlain = ""
    #get the plaintext for the childkey and score it
    for digram in digrams:
      childPlain += getDigram(digram, childKey)
    childScore = digramScore(childPlain)
    #Always replace a parentKey with a childKey if the childKey does better

    if childScore > parentScore:
      parentKey = childKey
    #If a childKey does worse, sometimes still replace parentKey with it to get out of local maximums
    #The bigger the difference between the scores, the less likely the childKey will take over
    #Grab a random value from the churn numbers
    #If the number is larger than the difference, continue with the childKey
    else:
      decider = randint(0,99)
      maxDifference = churnNumbers[decider]
      if (parentScore - childScore) < (maxDifference):
        parentKey = childKey
  
 

cipherText = "RUBQVPLPSZWCDRRQDTTOTFGBFRDASXRFRAISIBPCAWTWORPVQHWNOQBUABKXHVRDQBDSWAOGKRTOESQSCMOBGICNIERAMTSZOSIZABISSFIRTDFRESWKPDOBFWKRPCSFXSOBFWPRPSWAQSIRTDFRESWKPDOBGRPSAIFHBURFSDHQVPRGDTSQFHTOBICNBKVPIGFZECBKIUKFDIOSIZRQGTHOOBQBDSWAABPBDIHPOGPMKBGMIFIDOBRBYNFHOSAITZHGQGFXKIPCFRTPVSIFGFVFBUIOHQYXTRCSVAVIRTSOOBZSBNPTCSABPVKMFYKBDXKBOIFWXIQTISIGSQOSARRYQFYFDERKDIOFISTEOROSRODRRQDTTOYEZBRFXKAIETSCDBQBRAHFIAIAQNDAQCVSIFRTOSIOSEOFRTROFIPCRPQGKCFZIAZBACMNBZAIGFWKYCRKZBACMNBZAIFRTPOSOGPMKBGMAVDTOTFXISQBFRPVPHOBURMGSZLCFTDXOGQNRZFZPMTAPCOSIQRDFXIAFHFZAWPRZBSCABFRPRKSRPTDIOSZAIFHOFISTEORCSIFOBIWIEPTYWQHWFAVSXFMGTZROSRPNUAQQSVRIOIDAIVSIFGTZRLPSZBRFZDIOSAZPRZBSCABPCSFXCSZAQQSXRSXOBIAPTPDOBWKBXAIORGSGBSAHGRKCXOBIARTTDQGRPYGTPOSAZPRZBSCBOBUABRADEPWPRQCRKPTHTSZFBOSIKIXRQIGRAHFIAOSRQVSIFRTOSRQIFWAOGHOBDRZBPVPTDBZAIGSGBOFRKRQGDRKZRQGRBYNRPDTGBIAGRPSRIABPFSBFZMOTRPQFMTRNCYBGIQTTWTRHVAEPQBIHIKYRKFITORDQRXSRGSLHQGQEATWFWDZQOTORKCRAITOFTHGOGHOOBORQHQCTORKPTQCKZRODTSQTWTFGBYIDFOBORRKCRAIHCFKORZIYBTFHBETWFOFWFRFOSIZABISSFIRTDRPDOOBFWQSINAIFBNTRFIEPTYWQHWFRFIFSZAIFHOFISTEORTFPNDFBDRZFBOIZBISFBHDFKRAXRPVPHBQVPRFQHQCEYFETOSBIZBOWKCIIGRKYTFZISMADSOBCEIZAQLTBPFTTQOBIBIETOFOQBRPTBHRTZFQSQOSBOABZBWCURFRHVIOTQXFHFSRBIPDZSQGZTYIECVYRQOTHFIRBQEAXBQCOSIFIDOBZIBIOSURFRESWKCTLTAIAIIFOBISFBKRFBDXKBOITASCOSAIABPBEOPDFBOIMNTXORTFHOOBGHZTWRAIRGFAORMIDFOBZIBIOSGSDBQCRASXIZRQOSROWKRKPDOBGHZTPSOBZIBIOSTWTSIYSZSQOSBGTZSQURFRNVFKCSFZPCVSRDSVFZPMRASIZASQKMATOSIZABISSVRFWTLTAIRDBKATOSIZABISTVFBMIIZRQFYKBDPRTPFOBTSIYSZZXFZPMFBZBRAZIQRQHQCIFIGRKGIPVPBXDRDBKWKQBTWTOOBZIMNTXORBKURCFSGWDWAWIIGIFIFBDRZOBPSOBFWWRRFPTIADSKMWKGIISOBGRPSAIFHOSIGRTNFRGSQPDOBCEIZAQFNQRUSESDHOBEISIBUBQTOFBDIOSRQSEOSTOBIIKIXABIAMPSZAIRPOSROUKVSRQXBRZIGRPOSROFZOSOSRKTDPTPTLCSERQSEOSAIKMIADESQTWTRWNIOOBQSISSTFIBNEATFZBISOBQSISTLHQAEFIXIQIBITOHEIGEIRGHPKFEHZBRKHEORBWAIIFIDOBQSISTLHQARXFIDFTHGOGQRQHZTPAQCSAHGOSIZOZAFOFIEFIXIQIBITOHQEAAXTOIFIDOBSFIEEGKSESDHOBPTTUOAIAWNAEPSOBIKIXBIRQDXFTTDETQSHOOBQSISSTFIIEQRYMXDRKGYIAZIGRBIRTOFHPIZBZRQKZFOIGRKRODTYBOIOSIFIDOBPTTORKGRBIFZPCOSIZABISSVRFHFWAFVPCIAPDSFWFRKCTFIPTBEDTCWFOLPSZQRUIDSKMVSIFQBQCOSRFFIPTVYURHRXFTDYBMFBUARIZRQBRFZDISXFSWKCIIGKFICCRTBMSZSVKGCFUABIETOFOQBORTOBDIFABEHXFIDXRGROSRGWAWIRQHPKFDWGRXDIGTAYZIAOSOQIAZINFBZRQFBYIOSEIYIECVYRQDIOSIFIDOBZIBIOSYVTORAESWKYTSEVSGANHIGGOTFQRTASCOTIZIOOBFRBPTFYFTSTXGSDBQCHZAIOSBOSEEXSQRKGTPNMKIFAIORZIOSBOVKVPBIRTOFHPIOSFZYSOIDOBZIBIOSURTWTOIFETKRACRKPDFBDIOSROWKOSBGTZSQOSIQKBQROTRKPDOBTOBIHCHZIGRPDRSNVKBISEREOTBRFZDIOSIZABISTVOBRAPBBZIGOSRTRAYRWFBOAOBQOHSECMTORDBKIARFSQTOFBDIOSIZABISSVRFOSRGRQOIESHOOBWKBXAIORRKPDFBSDEIYWKBBCFOETWRRFOSBGFTDXAIOADSIDTBTRGIRURFBQBRSEIFIGAMXDHQBGDAPSOBORGSPCGRPSWAKFPTPSFEGSDLQBOIGSHCHQGQRDBKGHGIPHOBZIBIOSTOTZTGIFIDOBGRPSAIFWIWESWKGIMIGAEDSOTNOBIATOFBSDBIWIEAPDOBGHZTPSOBFWPSOBTOBIFRPCOSAOBXIQKBQROTLPSZKRDIOSIOBDBGAIYWACZBKWHCBITRXKTDAIRKCTIFWAPW"


churn(cipherText)
















"""
The following code was not used in the final method of getting the result. 
It was used for different methods that did not end up working for us.
It's included for reference.
"""


ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ALPHABETSTRING = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

"""
Prints all possible keys with given length for mappings set in this function
"""
def possibleKeys(length) :
  hsto = "HSTO"
  customAlphabet = "ABCDEFGIKLMNPQRUVWXYZ"
  keyParts = permutations(customAlphabet, length-4)
  for keyPart in keyParts:
    keys = permutations(''.join(keyPart) + hsto, length)
    for key in keys:
      newKey = "".join(OrderedDict.fromkeys(''.join(key)+ALPHABETSTRING))
      if not checkPossibility("TH", "OS", newKey):
        continue
      if not checkPossibility("HE", "OB", newKey):
        continue
      print(newKey)

"""
Check if plain could be mapped to code for key
"""
def checkPossibility(plain, code, key):
  plainLeftIndex = key.index(plain[0])
  plainLeftRow = int(plainLeftIndex/5)
  plainLeftCol = plainLeftIndex%5

  plainRightIndex = key.index(plain[1])
  plainRightRow = int(plainRightIndex/5)
  plainRightCol = plainRightIndex%5

  codeLeftIndex = key.index(code[0])
  codeLeftRow = int(codeLeftIndex/5)
  codeLeftCol = codeLeftIndex%5

  codeRightIndex = key.index(code[1])
  codeRightRow = int(codeRightIndex/5)
  codeRightCol = codeRightIndex%5


  if plainLeftRow == plainRightRow: #same row
    if codeLeftRow != plainLeftRow or codeRightRow != plainLeftRow:
      return False
    elif (((plainLeftCol != 4) and (codeLeftCol - plainLeftCol == 1)) or ((plainLeftCol == 4) and (codeLeftCol - plainLeftCol == -4))) and \
         (((plainRightCol != 4) and (codeRightCol - plainRightCol == 1)) or ((plainRightCol == 4) and (codeRightCol - plainRightCol == -4))): #right mapping
      pass
    else:
      return False

  elif plainLeftCol == plainRightCol: #same col
    if codeLeftCol != plainLeftCol or codeRightCol != plainLeftCol:
      return False
    elif (((plainLeftRow != 4) and (codeLeftRow - plainLeftRow == 1)) or ((plainLeftRow == 4) and (codeLeftRow - plainLeftRow == -4))) and \
         (((plainRightRow != 4) and (codeRightRow - plainRightRow == 1)) or ((plainRightRow == 4) and (codeRightRow - plainRightRow == -4))): #right mapping
      pass
    else:
      return False

  else: #different row/col
    if codeLeftRow == plainLeftRow and codeLeftCol == plainRightCol and codeRightRow == plainRightRow and codeRightCol == plainLeftCol:
      pass
    else:
      return False
  return True

"""
Prints the digram frequencies of a text
"""
def getDigramFrequencies(text):
  alphaText = ""
  for letter in text:
    if letter.isalpha():
      alphaText += letter
  second = False #true if on second letter of digram
  noDoublesText = ""
  prev = ""
  #Insert X where needed
  for letter in alphaText:
    if not second:
      noDoublesText += letter
      prev = letter
      second = True
    elif prev != letter:
      noDoublesText += letter
      second = False
    else:
      #second stays true, prev stays the same one
      noDoublesText += "X" + letter
  digrams =  []
  prev = ""
  index = 0
  digrams =  [noDoublesText[i:i+2] for i in range(0, len(noDoublesText), 2)]
  c = Counter(digrams)
  #print(c)
  print(c["IB"])
  doubleDigrams =  [noDoublesText[i:i+4] for i in range(0, len(noDoublesText), 4)]
  tripleDigrams =  [noDoublesText[i:i+6] for i in range(0, len(noDoublesText), 6)]
  quadDigrams =  [noDoublesText[i:i+8] for i in range(0, len(noDoublesText), 8)]
  quintDigrams =  [noDoublesText[i:i+10] for i in range(0, len(noDoublesText), 10)]
  hexDigrams =  [noDoublesText[i:i+12] for i in range(0, len(noDoublesText), 12)]
  noDoublesText = noDoublesText[2:]
  doubleDigrams2 =  [noDoublesText[i:i+4] for i in range(0, len(noDoublesText), 4)]
  tripleDigrams2 =  [noDoublesText[i:i+6] for i in range(0, len(noDoublesText), 6)]
  quadDigrams2 =  [noDoublesText[i:i+8] for i in range(0, len(noDoublesText), 8)]
  quintDigrams2 =  [noDoublesText[i:i+10] for i in range(0, len(noDoublesText), 10)]
  hexDigrams2 =  [noDoublesText[i:i+12] for i in range(0, len(noDoublesText), 12)]
  noDoublesText = noDoublesText[2:]
  tripleDigrams3 =  [noDoublesText[i:i+6] for i in range(0, len(noDoublesText), 6)]
  quadDigrams3 =  [noDoublesText[i:i+8] for i in range(0, len(noDoublesText), 8)]
  quintDigrams3 =  [noDoublesText[i:i+10] for i in range(0, len(noDoublesText), 10)]
  hexDigrams3 =  [noDoublesText[i:i+12] for i in range(0, len(noDoublesText), 12)]
  noDoublesText = noDoublesText[2:]
  quadDigrams4 =  [noDoublesText[i:i+8] for i in range(0, len(noDoublesText), 8)]
  quintDigrams4 =  [noDoublesText[i:i+10] for i in range(0, len(noDoublesText), 10)]
  hexDigrams4 =  [noDoublesText[i:i+12] for i in range(0, len(noDoublesText), 12)]
  noDoublesText = noDoublesText[2:]
  quintDigrams5 =  [noDoublesText[i:i+10] for i in range(0, len(noDoublesText), 10)]
  hexDigrams5 =  [noDoublesText[i:i+12] for i in range(0, len(noDoublesText), 12)]
  noDoublesText = noDoublesText[2:]
  hexDigrams6 =  [noDoublesText[i:i+12] for i in range(0, len(noDoublesText), 12)]

  cDouble = Counter(doubleDigrams+doubleDigrams2)
  cTriple = Counter(tripleDigrams+tripleDigrams2+tripleDigrams3)
  cQuad = Counter(quadDigrams+quadDigrams2+quadDigrams3+quadDigrams4)
  cQuint = Counter(quintDigrams+quintDigrams2+quintDigrams3+quintDigrams4+quintDigrams5)
  cHex = Counter(hexDigrams+hexDigrams2+hexDigrams3+hexDigrams4+hexDigrams5+hexDigrams6)
  #print(cHex) #pick something to print
      


"""
Find frequent digrams of which the reverse is also frequent
"""
def reverseInfo(text) :
  digrams =  [text[i:i+2] for i in range(0, len(text), 2)]
  c = Counter(digrams)
  appearingDigrams = list(c.keys())
  for digram in appearingDigrams:
    reverse = digram[::-1]
    freq = c[digram]
    reverseFreq = c[reverse]
    minFreq = min(freq, reverseFreq)
    if minFreq > 60:
      print(digram, minFreq)


"""
Split the text into digrams, making it easier to read
"""
def splitPlayfair(text):
  digrams =  [text[i:i+2] for i in range(0, len(text), 2)]
  splitText = ""
  for digram in digrams:
    splitText += digram + " "
  print(splitText)
  return splitText


"""
Try to decode a text using the given decode map
"""
def tryDecode(text) :
  decodeMap = {"OS": "th", "OB": "he", "AI": "in", "IZ":"er", "BI": "is"}
  
  decodeMap ["FZ"] = "wi"
  decodeMap["RO"] = "us"
  decodeMap["RK"] = "at"
  
  #decodeMap["TO"] = "is" 

  
  #decodeMap["B?"] = "TB"
  #decodeMap["DI"] = "sa" 
  
  
  digrams =  [text[i:i+2] for i in range(0, len(text), 2)]
  result = ""
  for digram in digrams:
    if digram in decodeMap:
      result += decodeMap[digram]
    #check if opposite digram exists
    elif digram[::-1] in decodeMap:
      result += decodeMap[digram[::-1]][::-1]
    else:
      result += "__"
  print(result)
  return result

"""
Check for digrams frequently following/preceding a specific digram
"""
def getSpecific(text): 
  digrams =  [text[i:i+2] for i in range(0, len(text), 2)]
  next = False
  followingDigrams = []
  precedingDigrams = []
  prec = ""
  for digram in digrams:
    if next:
      followingDigrams.append(digram)
      next = False
    if digram == "OS":
      precedingDigrams.append(prec)
      next = True
    prec = digram
  following = Counter(followingDigrams)
  preceding = Counter(precedingDigrams)
  print(following)
  print(preceding)

