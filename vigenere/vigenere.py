from collections import Counter
from itertools import permutations

"""
For an (untransposed) text encoded using Vigenere, find the likely key lengths (no higher than maxLen)
To do this, for each possible key length, the index of coincidence is calculated. (http://en.wikipedia.org/wiki/Index_of_coincidence)
As monoalphabetic ciphers don't change this value, each set of letters encoded using the same keyword letter will have the same value
as without being encoded. If all of the sets have a fairly high index, this key length is probably right
The user should tweak the minIndex value depending on the language of the plaintext 
(e.g. 1.6 for English, 1.9 for French and German, 2 for Dutch, ...)
"""
def getVigenereKeyLength(text, maxLen):
  minIndex = 2 #USER CAN TWEAK THIS VALUE DEPENDING ON EXPECTED VALUE
  indices = {} #dict mapping key lengths to index of coincidence
  for length in range(1,maxLen+1): #Try all key sizes up to maxLen
    subTexts = [] #will hold all sets of letters encoded using the same keyword letter
    avgInd = 0 #average index for all sets with this key length
    for j in range(length):  #generate the sets
      subText = ""
      index = j
      while index < len(text):
        subText += text[index]
        index += length   #always skip keylength chars ahead in the text
      subTexts.append(subText)
      c = Counter(subText)     #get the frequencies (absolute)
      #get index of coincidence (see wikipedia page for the formula used here)
      freqSum = 0
      for freq in c:
        freqSum += (c[freq] * (c[freq]-1))
      div = len(subText) * (len(subText)-1) / 26
      avgInd += freqSum/div
      #end of index formule

    avgInd /= length  #avgInd was sum of indices, divide by number of indices for avg
    indices[length] = avgInd
  #Store from highest to lowest index
  sortedIndices = [(v,k) for k,v in indices.items()] 
  sortedIndices.sort(reverse=True)
  found = False
  #Print all key length / index pairs that are high enough
  for v,k in sortedIndices:
      if v > minIndex:
        print("Key  length ", k, " gets index ", v)
        found = True
      else:
        break #ordered by index, no more above minIndex will be found
  return found


"""
Calculate the expected key length for a text encoded using Vigenere followed by a single column transposition
For all numbers of columns up to maxCols, all possible Vigenere ciphertexts that could end up in this text are generated
and run through the above function to determine the expected key length. If a wrong transposition was undone, no possible
key length should be found.
"""
def getColumnTransposedVigenereKeyLength(text, maxLen, maxCols):
  #Attempt all numbers of columns up to and including maxCols
  for cols in range(1,maxCols+1):
    print(cols) #useful to see how far the function is during execution
    colOrder = range(0,cols) #ordered list of the columns
    #generate all possible column orders for cols columns
    colPermutations = permutations(colOrder)
    #count number of columns with "extra" character (== number of columns with bottom cell filled in if some had to be left blank)
    biggerColCount = len(text) % cols 
    charsPerCol = int(len(text) / cols)
    #For every possible column order...
    for colPerm in colPermutations:
      biggerCols = []
      colMap = {}
      #Generate list of cols with "extra" char (always the left ones in the untransposed version)
      for i in range(biggerColCount):
        biggerCols.append(colPerm[i])
      index = 0
      #For every column
      for colNr in range(cols):
        #Grab the col (they are in order in the transposed version)
        #Take one extra character if it's a "bigger" column
        if colNr in biggerCols:
          thisCol = text[index:index+charsPerCol+1]
          index += charsPerCol+1
        else:
          thisCol = text[index:index+charsPerCol]
          index += charsPerCol
        colMap[colNr] = thisCol

      #Now convert the columns to an untransposed ciphertext
      vigenereText = ""
      #In the permuted order, pick one character from each column, repeat until text fully formed
      for index in range(len(text)):
        vigenereText += colMap[colPerm[index%cols]][int(index/cols)]
      found = getVigenereKeyLength(vigenereText, maxLen) #Check for possible key length
      if found: #if possible key length found, print used column order and resulting untransposed text
        print (colPerm)
        print(vigenereText)

"""
Using a known key length, decode the ciphertext into the most likely plaintext
"""
def decodeVigenere(text, length):
  #Analog to getVigenereKeyLength, get sets of letters encoded with the same keyword letter
  subTexts = []
  distances = []
  for j in range(length):
    subText = ""
    index = j
    while index < len(text):
      subText += text[index]
      index += length
    subTexts.append(subText)
    c = Counter(subText)
    #Get the most frequently appearing letter
    #This is extremely likely to be the substitute for E, especially in Dutch    
    orderedC = c.most_common()
    eSubstitute = orderedC[0][0]
    #Get the positive distance between the substitute and E, this value allows us to decipher any letter in this set
    if ord(eSubstitute) < ord('E'):
      distance = ord(eSubstitute) - ord('E') + 26
    else:
      distance = ord(eSubstitute) - ord('E')
    distances.append(distance) #store the distance

  #Now generate the plaintext
  answer = ""
  #Rotating through the subTexts, grab one letter from each, and undo the correct offset
  for index in range(len(text)):
    letter = ord(subTexts[index%length][int(index/length)]) - distances[index%length]
    if letter < 65:
      letter += 26
    answer += chr(letter)
  print(answer)




#maxLen and maxCol were set through trial and error
cipherText = "RGNYKSFKOJZXKHSNNCHBQTRNQCINOPYXKCEJAGXNBTZDTCVPZCKWYSPCUPINGJXPJXWTNCXCTWJJTCDNQPRTOTKYKCXUOIMJXSIAKSVEAXESKTERKTIPKYSNKYHXTIIPZTQRYGKMTXSCFDWNQBSCPIINSPVWTCRSJAWMZCIXKKOXIDIUOWIAPARNKXINZHPNKPIKYDIXKTVUHPENGJTEQPIRFDXRXKPWTZMWGBPBKSDWAQVOPJTKVNJIVJROUPWESFKVTJWELJFIOBYIPBDXLSEVGXZIKWWSPNAWLRWXTTLTUJNSUYYRLWLRSSFHHTBNDIFFAFLIORWRZWGXKMWXLLWIJFGILSKQZJHILFSEKJXWPGYAYJWAKSCPIXWIYMAXYXNVSHLRKJGKNYJEHNKILJWTHEVIYRLMVJGTLSGILNJXYFATPSFRRJBPPNWXKSGSAGFJLNMIIPKILMVHOLLGKRYWXVIGHRQVRLOSRCFZRLMYVDZJPLFYXHTKXAJGMHZSIHYWMUJVDKEAVIXGRIUGXPWHSLSSEVJLRLJFVOSGVAJVVZPFXUYSLUYFQAIAMILEMABKVPTMMPSNMWQJTAWZXBSKITAFVVXYISSSMZLFOKTWMLJAVLSAMLSLHLJESKMWXBRWMUJCTYALJLFRKUADRCIGPPTWITBNHGFWRKYFIOTEIZJWIPWWXAAJWMBMFEVJFHHYJXTYWHLYWVKYWHTPFWYUAWYFMHLSSRLBYHCJBMYILIKXKXSYVMHNNNAQWHLJYSPWVKPRLZQYKILIDSPNCMQFSILIEILFMWJTLYHXFVSJFFAJLOLSKIUTWRPJYIUFYHVTAJLJBWWZCSOSGETFKYUMWIKIRPUYEIVWZRAPWMPXFEZSDOLSWTDXFTYFLSRNNXCNAEHSFPHJAXYJAVKQNPPMYXLMSIPTIJZDMRPCXNXTRKZDPRCTSATPOLOTXCGZQWJTEATTIUXSZDBDENOJIAXAPSTTXWTPVJFZRNKYNNTCNSYXHMKPGXKTERKTKNTTMAGRIAKTICNGIWTWETZJLUTCPJGCEUGDXNITIRGTHUGTLDGDSTTAMNKXXXMTXTNTLNSJXNYCOPTCRAKGSNBQINPBINUTATXDNCKTRWSYRTMSRJKYNWRTYNQDICGSIPTQRYTHINKRQXIKZTKQKCQYKBVVKCINJKFUKTEQNLHWKQRAKBRWGGHNKTRNTDINCLXCFUQNZEIXYPMCKGINUYINKYORUTHCTIIMMCKURZVJBCINVIRATWJBXIWPUXFNKDRPUGHUBBIUUHRNTJEXJGRSJCRNHIYNXTINXDPNOTEICPERKLENXBKCJHAAPZINGZQMNALNUTHIGHEJXDDNOTNSXGDIRGRTJDXSKTMUKVINKISCZC"
getColumnTransposedVigenereKeyLength(cipherText, 9,6)
print("\n\n\n")


#This untransposed text and key length was found through the above function
untransposed = "KTORWRSILGMQDJLNBXWZGYMIADKKFKQMRSEZVRYFVTOPWKJKPCXOFQJXVJHKTNIZHCKXGXYQVTHKJYNRRHXKJKQSTBIZVNYVVDRNWVJPLCHKRROHLCOCSBYIUTRQWNPSCTVJWAFRKKETZNYFSPRQWUFOLCHKKLMITTVOYNPETTVOFQJXDPWNWCZYYLEGJXUHLZPKAWJQLCWKFWFEYQIJYJFROTXAMABEHGHKYATXLBITKNSRPTXBSWBIATRGDUJZLGXXGDBHLSMTYNSZHCHKEDZVCTVBSPJRGDIZBNXEHCMTZNYKYDIOWWIIKJMYLNWIUSICWAJPKLSXVCXXPADUKCNPKPXFASEISUWTANYQLTVGVNRXIJMZWWXXHEXTGPNITPRJNXTVIXNYLJUWAPTFGTQMUZXNWCJRPCHKNNWXLGSKHCJIUYSTYNYNLWSUYNSJPYRTSJWILCETVNWNVCKKLSJDPYRYLNROSXRQLRSHLPZUFMJRQTHKFTYHHPVOKCTGOTITBXSKLINKGYIIDTVKDMIEACSMFRJXPCFKVUNKATVOCUFKZIMRLNPMQZITFJFVOTXXSJRMUSIBWAYILCRGSAIIZRLKENWIUSIVGAYVLIXKFEFRKTQAMAMIAXWTWCIEJWXNASTJLGMKLBLIITYXWWLEHIITERXWJWMKFPFEATVUGTBISXIZKPJFLJVKFNSLPYFKKUTSADQTMNJRZCMKLPJPPYOUHJSHLGIGNXSHLCMTKUFEWIIBSUQIUBEGJPTIKDTZWUJXATRUXNWQPHWIZRJRPTXYYNGIBGITYRSKUJAGKMFEYTITYXJHTXHJWUASVGAGFCTRKTVFASSLVDJJCDXWLCPGYNJRIDIQBNXSSBWHWTSSWIITSCZYYAMPCNMMZISXANLIOTXKFNSIYXOSGNXXKPEXNXTVTDVMWWFPSTMTKNHXLCYOLTJRUTRNASMEKTVJWIJLLAICGNSWKPKSAMIENJMZRRYXLCPKJNSIULEYLXYEHCHKENNOLKIXKPJOVBITEXWKLCSIZCJRKDRJWAMIAHTKWUPAHGXOWAESBWMPVNRIPZIBWAXIYQMPFNRIUAEGLNJRZZMPCNSQVBTKDMJIYXONGNAILATULNSLLTJZWNSALHTUGTFPDTIXRNXHLDKKFINNUPTGJCAIYHXKDKFEYTRYLJFRCDSXAWIIRDTSGXNDPYPKNNSRPTXOFTTVCTRMWUNNRSIHASJRTPEXBJBEHGPKNNSDPYHGFINNGJPRWWFTHGXRWEJRKTRQATSYKPXJGNYIYDSQFRJXADIFASGIODVKFCTXKTJGERQMLSIXNUNIZKPKMPJPPVITWWMIIQITYNPRPZXKKYWMLIITWWMSLHXGSCMIABIZVNAPPCHKJB"
decodeVigenere(untransposed, 8)



