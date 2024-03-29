import copy

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def getPossibleCribLocations(cipherText, crib):
  for i in range(len(cipherText) - len(crib) + 1):
    possible = True
    for j in range(len(crib)):
      if cipherText[i+j] == crib[j]:
        possible = False
        break
    if possible:
      print (i)


edgeSet = set([])
lettersToCycles = {}
def getCycles(edges):
  for letter in alphabet:
    getCyclesInternal([], edges, letter, letter, [])

def getCyclesInternal(soFar, edges, start, end, visited):
  newSoFar = copy.deepcopy(soFar)
  newVisited = copy.deepcopy(visited)
  for i in range(len(edges)):
    if i+1 in soFar:
      continue
    if end in edges[i]:
      if edges[i][0] == end:
        other = edges[i][1]
      else:
        other = edges[i][0]
      if other in newVisited:
        continue
      nextSoFar = copy.deepcopy(newSoFar)
      nextVisited = copy.deepcopy(newVisited)
      nextSoFar.append(i+1)
      nextVisited.append(other)
      if other == start:
        #print(nextSoFar)
        cycle = tuple(sorted(nextSoFar))
        if cycle not in edgeSet:
          for j in range(len(nextVisited)):
            letter = nextVisited[j]
            if letter in lettersToCycles:
              lettersToCycles[letter].append(nextSoFar[j:]+ nextSoFar[:j])
            else:
              lettersToCycles[letter] = [nextSoFar[j:]+ nextSoFar[:j]]
        edgeSet.add(cycle)
      else:
        getCyclesInternal(nextSoFar, edges, start, other, nextVisited)


cipherText = "KRVKFDIATNHZRKDOAURJTIHCKOCVYPLLDVGVYMUFQBQOKLOUCARCDKDFYODGGBLZSKMDBOQRYYJNRXFZEMABTJBSCSUKJCZSLEKYBAFOFRDIPZPDYJLOVYTJEERJOLTDFWVRVBVJXSOPXTUWWKLVVCGNROQANPCAAJRRZHZZNZXUSZWWASMBWBKIMYNGLXHLBHDUXHZXKDYVCOYDJLNJAXSWHPTKLUAYTVENAUOAVZXLSPQEOSJZIPSEXWUBYJDDPCTIWDQCWBSDQSUPVWTLGKLYWYSTUTXZEWVXFUQUYWWPQRWUAMSVAMDJYNXRWMWXOPOQNZGIPMVBKHZHYCVAVABFMCHZCJUSSOAJHGHRCASWLQCVOCLLSNBOXWJNJQZGVDOBRQAAYWKACXNQMXQIMZTFJZWOZSCGGDYRKHLVDBUZYKKFXFMZJJAZAMCGUBDPGVMOVEJAYKFADJKRXUSOYBQYZUZGXGQEVIATXLYKNYNZQILQWOTDIKMWPIBVVQLUOWZEENVVYIMZOIPHXLKFOZQVRIOZYBLLVDHWBFPYKAOCQVOSURSCUQXFKSRQFHBZQXXCPMXFYVPHLWVGUELRNZQRDNOMYLSOJRZUKSYSPEVVWWBYABXTBGUEWTCWYERYMUWFJNCEQHFNODXGHJMEBRGDYGHAUJHIXMMKLUROGFTMSTVIFWLQBPOWSZXUPYCTMRMVUMXCCEOHHDJTCDJWQYKQJCXJSKVOCUMIUIXABEKAVIZEFSGJFCJWCPRTUGVQLULMAHJXWDTVGKYLJVUMTFCTQJZSTMVQIGIIMGFJOLXKULWMZSKBCRJZNIXXWMDTFTAJQZOFWXQAAMMTDVYBKWWSIWCCBXFYISMKRMFOSEQQRFQDQXYAFHEDXTFZBXOADZFMRJGUODBBWIXZMCIGHJPZVSVZBDLASAURSRLHXASHBCNONZNLUBXPEFPNRRHBAXDMUDMWMMCNZQTMYKBIUSAPLSLURTLAFGCVOCZLAXFVXKUFFXTBBUNFAQFFWVMCDABXKJOEAXUZXHAVRVYASDYXEJPOMDFICNFPMTIWMJPHFBNDHPGQPLBQZEEQTZNJTXHQEQESJOTNPFFUKZPXUJCTLMLGVCRPMSXFBYOKSCVXUGZHSSAVCQYGZDHKZPYSSGTCEJKGBDSQUZXSMRZHDZOLMIGOADKMPUMWGFNPVLVNLJOQSXHQYVOZUYSYQHYZWXEPVUTTNZCGTFBQOLOKSIJNFRTXOAEFQXXYOWDUYKTXWEABJJXKMXNWKUDDXTLVDGEQBYPXCUBTRNVJOHGNQBTUGHBOLNNXUABVPWKQDWFKHDUEILXANSJFJUIBCBHBFFEKLQPGAXUVUOOVZTGJWKLBJOTALGDUIFHPIXAOJAVVYQVLARSNEGWRNHICNISVDQVZOLHQIIXHXTMHCVEHERLIKFHNUFGCLYKELRWYXHGGGIUOESNHCSGOFGQLHWPJBFXGGOLMCIBVNKGMURBWNVFAWBKYESVBIGKAWYDLEMOUNJNSGEJOBDBTUMVNIWEAVAYZLQGVDNYFTSUDODOUDRZEOPWXBLORZEWXDFCKXWOYERGRDWPREPINPTMZTQUASGVQSESFPNCYPFSNYIFNROAUUALWVQGBEWGJZAIPFPRCUVBKKLJBUKIVDMZSZIDKQGVYBRWFFYPLFWBSBMWKYFDJVLMYISOMWTNCMXXOTUXKWMQEDUDGWJLLWEHOTRGCVJBRGKVKOYVXBEYUIGZGGLDCLYPNBRKKVOJAXTGDSDJMIHCHYFMCJKKIPDVJYYWEVRRUPURYZJZCZDDJGFFCKBRYJWBSQOXUWFVWSTVQKUWHEWOIHRQHKJJLYUIKOVRNKYCIJZQVLOGMKMJMQOJDVRKBCWBQSDOTKBFVRNBFJUFCSLPLTMZQRBQPQYYYHTTTSGRGYKJQUHEHHZZTDSSKBMHZQYSKMQYYCJGLGAVEYAZQHUEKQQHGKIQQHHGRTIICVIHNIGMIEPOJAGUTHDYLPVTATKFATYDHFIGKYFKWYHLVGXWJBFBLTPUTIZZMPAIYGIESDCUHZLJNWFZKOAFPIEZHBMMYWCGGESHKASYWTZGQMDBKMYZAVXGEZYBFSOEMTWMXAVDNROQEPZAFDBWRNIWVKVJCDMCIYJZHFJNJLYPKMNHVMWDDZGRDDSTCXVMDEKEGTMWQPMEYWMPKULVZHCSPWVFAXXSAGBUYVTGKALZWVNJCKVVYKLFRZFIYMZEGJNMBQTQGHNVWGAOEJVQKYJHDQBXGKTOTPRZZMWSPEMCSXNTADOYITCUEYFDDGAVELDTBFVHRWGZHNYRGOIBENWDRJKZDQBIXFARWKGNAGOMYTUBPLKKPJOPTCKNFMOHIGHXGMLHIYXCSFSJQRNDLTGPYQZTUMRIPJDZWTDHRTSJWUXVUDFMZNTXJVXXANZGIFUFGRMOENQJYFSRBTWLNRACHYGMUPDMHJHYWQVLMUAOXSWUFVCZOOYXQLIBYDFJUTFNVQDAKZSEITBDYMIJSFLDTRAYQSXQIGTZEUDKSUNURRJTYUTGRDGXDOWXIXHTWBSHHNLIVEGCAOTHRZOYEJWNBPQTYXXPKBYBHZBXZTOJYDESRWRWGTEDAODQDMQBIFQPOAMFMMMGBXAXANYEQRBOUUZPLXZHGOCYSMEFOQKTQJWDEZICCPKXLOHSVPJWQLIAZTEETFOVYPMSTHTASETJVORYGIPKKBSZRKPAQAROIKNYIGDPXZNNAGXQVDPQKQSZIJOFXQWMOFHHYCUUMTDJONADQGFYSEFGTIJJCJMAQCYFODKFYWTTNRYELAIQEBINRKOJNNFJVQKVUNFLEYUQFIAXLCJSYYISPFNMKGFOCWNIEQFLJOPEBWHWDIAMVFSDFRLQWJFZQETJICZWBLKOBDERKNPKDEYYXFPFUWURNVFFSWFJQCSSZDTOWZWWWKSVWEKLFGIFEAZOYOAWBOYWCONWQJAGCOZBPYWKRIKUOBPOJXSNXWYYFKZEOFHWRBKDFIIGYCINTGFGHYRBKMSGWXHZVABTNQYPOCNNWNFHBMTBGTJQURABVSPSSDVOWEAFMDKCFZQPSLOGFGKQZTPFKBIFIUPUGZOGTKHVQCQWRCTRNDYRPHRFDLEHPXYGDGOZIVKMWIQIYXBOFFBAQEMNNAEPBBGKNICAUIPYJKUNRHGKBQEEYJZEFWTFNHPKKYJPLCYPPSYGRMDIUDRLRULIZDQRDQGPFGCNXQMMCVAXDGTFWHEBGDSQVLCVVFKFYFLBVADTPOGEXSACHWLOLKSUWSMFOCPULZRZQBKLZVGQIQOIESAVHIRVDAZTMMBBWJVURPAZVVZNOQCLOHZYIPVWKWAVZSXDQPLZHOPJOLFVDWCSYIQOAEEXHPJTLWAPESKQAEEQNFYTWDFCJREHVFZRWNJPLBKLUHUEONBRAKVTLGRIEDUYLLXXDYVWJHLFCFQTFCJDJVOBVOMDAJVLVJDLRFANNWRXBUPDSWBLYTCUHWARAWOFMTIEARRWCWEWZGRYDWWRNNBGSZBRQWZVCCHPVRCZXMWQTSBBGIAOCPBZFOIZHMZBFLVQCMGUV"
crib = "VIELSPASSMITDIESERUEBUNGAUFENIGMA"
#getPossibleCribLocations(cipherText, crib)

edges = [("K", "V"), ("R", "I"),  ("V", "E"),  ("K", "L"),  ("F", "S"),  ("D", "P"),  ("I", "A"),  ("A", "S"),  ("T", "S"),  ("N", "M"),  ("H", "I"),  ("Z", "T"),  ("R", "D"),  ("K", "I"),  ("D", "E"),  ("O", "S"),  ("A", "E"),  ("U", "R"),  ("R", "U"),  ("J", "E"),  ("T", "B"),  ("I", "U"),  ("H", "N"),  ("C", "G"),  ("K", "A"),  ("O", "U"),  ("C", "F"),  ("V", "E"),  ("Y", "N"),  ("P", "I"),  ("L", "G"),  ("L", "M"),  ("D", "A")]

getCycles(edges)
for letter in alphabet:
  if letter in lettersToCycles:
    print(letter, len(lettersToCycles[letter]))

for path in lettersToCycles["I"]:
  print(path)
    
