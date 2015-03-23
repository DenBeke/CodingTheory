package playfair

import(
    "fmt"
    "strings"
    "math/rand"
    "sort"
    )

// A struct to make use of the Playfair square
type PlayfairSquare struct {
	square      [5][5]rune
	positionMap map[rune][2]int
}

func (p PlayfairSquare) GetPos(r rune) [2]int {
	if r == 'J' {
		r = 'I'
	}
	return p.positionMap[r]
}

func (p PlayfairSquare) GetRune(x, y int) rune {
	return p.square[x][y]
}

func (square PlayfairSquare) Encrypt(s string) string {
    retText := ""
    pos1 := square.GetPos(rune(s[0]))
    pos2 := square.GetPos(rune(s[1]))
	var newLetter1 rune
	var newLetter2 rune
	if pos1[1] == pos2[1] {
		// zelfde rij:
		// kolom+1
		newLetter1 = square.GetRune((pos1[0]+1)%5, pos1[1])
		newLetter2 = square.GetRune((pos2[0]+1)%5, pos2[1])
	} else {
		if pos1[0] == pos2[0] {
			// zelfde kolom: rij+1
			newLetter1 = square.GetRune(pos1[0], (pos1[1]+1)%5)
			newLetter2 = square.GetRune(pos2[0], (pos2[1]+1)%5)
		} else {
			// andere rij en kolom
			// neem hoekpunten van de rechthoek
			newLetter1 = square.GetRune(pos1[0], pos2[1])
			newLetter2 = square.GetRune(pos2[0], pos1[1])
		}
	}
	retText += string(newLetter1)
	retText += string(newLetter2)
    return retText
}

func (square PlayfairSquare) Decrypt(s string) string {
    retText := ""
    pos1 := square.GetPos(rune(s[0]))
    pos2 := square.GetPos(rune(s[1]))
	var newLetter1 rune
	var newLetter2 rune
	if pos1[1] == pos2[1] {
		// zelfde rij:
		// kolom-1
		newLetter1 = square.GetRune(Modulo((pos1[0]-1),5), pos1[1])
		newLetter2 = square.GetRune(Modulo((pos2[0]-1),5), pos2[1])
	} else {
		if pos1[0] == pos2[0] {
			// zelfde kolom: rij+1
			newLetter1 = square.GetRune(pos1[0], Modulo((pos1[1]-1),5))
			newLetter2 = square.GetRune(pos2[0], Modulo((pos2[1]-1),5))
		} else {
			// andere rij en kolom
			// neem hoekpunten van de rechthoek
			newLetter1 = square.GetRune(pos1[0], pos2[1])
			newLetter2 = square.GetRune(pos2[0], pos1[1])
		}
	}
	retText += string(newLetter1)
	retText += string(newLetter2)
    return retText
}

func NewPlayfairSquare(codeWord string) PlayfairSquare {

	// clear the codeword of any whitespace
	r := strings.NewReplacer(" ", "")
	codeWord = r.Replace(codeWord)
	// set all characters to uppercase
	codeWord = strings.ToUpper(codeWord)
    // change J to I:
    r2 := strings.NewReplacer("J", "I")
	codeWord = r2.Replace(codeWord)

	s := [5][5]rune{{'A', 'A', 'A', 'A'}, {'A', 'A', 'A', 'A'}, {'A', 'A', 'A', 'A'}, {'A', 'A', 'A', 'A'}, {'A', 'A', 'A', 'A'}}
	p := make(map[rune][2]int)
	fullCode := ""
	// remove duplicates from codeWord
	for i := 0; i < len(codeWord); i++ {
		seen := false
		for j := 0; j < len(fullCode); j++ {
			if fullCode[j] == codeWord[i] {
				seen = true
				break
			}
		}
		if !seen {
			fullCode += string(codeWord[i])
		}
	}

	// Add remaining letters to codeWord
	for i := 65; i < 91; i++ {
		seen := false
		adding := rune(i)
		if adding == 'J' {
			adding = 'I'
		}
		for j := 0; j < len(fullCode); j++ {
			if rune(fullCode[j]) == adding {
				seen = true
				break
			}
		}
		if !seen {
			fullCode += string(adding)
		}
	}

	if len(fullCode) != 25 {
		fmt.Printf("Problem with CodeWord %d \n", len(fullCode))
	}
	// setup square and positionMap
	for i := 0; i < 5; i++ {
		for j := 0; j < 5; j++ {
			s[i][j] = rune(fullCode[5*(i)+j])
			p[rune(fullCode[5*(i)+j])] = [2]int{i, j}
		}
	}
	return PlayfairSquare{square: s, positionMap: p}
}

func Playfair(text, codeWord string) string {
	if len(text) == 0 {
		return ""
	}
	// clear the text of any whitespace
	r := strings.NewReplacer(" ", "")
	text = r.Replace(text)
	// set all characters to uppercase
	text = strings.ToUpper(text)

	// setup the Playfair Square
	// NOTE I = J
	// Store in a 5 x 5 array
	square := NewPlayfairSquare(codeWord)

	// Put the X's between equal letters.
	newText := string(text[0])
	prevLetter := text[0]
	for i := 1; i < len(text); i++ {
		if prevLetter == text[i] {
			newText += string('X')
		}
		newText += string(text[i])
		prevLetter = text[i]
	}

	// if the number of letters is Odd, add an X to the end
	if (len(newText) % 2) != 0 {
		newText += "X"
	}

	retText := ""
	// take digrams from the text.
	for i := 0; i < len(newText); i += 2 {

		retText += square.Encrypt(string(newText[i])+string(newText[i+1]))
	}

	return retText
}

func PlayfairDecode(text, codeWord string) string {
  if len(text) == 0 {
    return ""
  }
  // clear the text of any whitespace
  r := strings.NewReplacer(" ", "")
  text = r.Replace(text)
  // set all characters to uppercase
  text = strings.ToUpper(text)

  // setup the Playfair Square
  // NOTE I = J
  // Store in a 5 x 5 array
  square := NewPlayfairSquare(codeWord)

  retText := ""
  // take digrams from the text.
  for i := 0; i < len(text); i += 2 {
    retText += square.Decrypt(string(text[i])+string(text[i+1]))
  }

  return retText
}


/*
Try to find the best possible square, using the hillclimb technique:
first generate a couple (100) of random squares
keep 5 best. and breed these.

Best: those with the highest IC in the text
breed: create random permutations of these 5 squares

returns the best key found
*/

func HillClimbCrack(text string) string {
    // create the 100 random squares
    squareStrings := make([]string, 100)
    for i:= 0; i<100; i++ {
        intArray := rand.Perm(26)
        // construct the square corresponding to this array
        newSquareString := ""
        for j:=0; j<26; j++ {
            newSquareString +=string(rune(intArray[j]+65))
        }
        fmt.Println("%s \n", newSquareString)
        squareStrings[i] = newSquareString
    }

    // Filter out the 5 best
    //  Decipher text and calc IC, higher IC is better
    squareStrings = FiveBest(squareStrings, text)
    /**
     * iterationStep:
     * generate for each of the 5 best squares 1000 random successors
     * by randomly swapping 2 letters.
     * keep again the 5 best ones and continue. Until a max is reached and the newly generated ones are not increasing in IC value
     */

    notReady := true
    maxIC := 0.0
    best := ""
    for notReady {
      workingSquareStrings := make([]string, 5000)
      for i:= 0; i<len(squareStrings);i++{
        // generate swap pairs
        for k:=0; k<1000; k++ {
          currentSquare := squareStrings[i]
          randomNr1 := rand.Int() % 26
          randomNr2 := rand.Int() % 26
          // swap letter at pos 1 with the one at pos 2
          tempRune := rune(currentSquare[randomNr2])
          ReplaceChar(currentSquare, randomNr2, rune(currentSquare[randomNr1]))
          ReplaceChar(currentSquare, randomNr1, tempRune)
          workingSquareStrings[(i*1000)+k] = currentSquare
        }
      }
      // Select 5 best
      squareStrings = FiveBest(workingSquareStrings, text)
      // check if any improvement is made.
      // If the max of previous is less than max of current stop and return the square string.
      newMaxIC := CalcIC(PlayfairDecode(text, squareStrings[0]))
      if (newMaxIC < maxIC) && (maxIC > 1.6) {
        break
      } else if newMaxIC > maxIC {
        maxIC = newMaxIC
        best = squareStrings[0]
      }
    }
    return best
}

func CalcIC(text string) float64{
  // Do IC analysis on decodedText
  var IC float64 = 0.0
  for i:=65;i<91;i++ {
    if rune(i) == 'J' {
      continue
    } else {
      c := strings.Count(text, string(rune(i)))
      IC+= float64((c*(c-1)))
    }
  }
  IC = float64(IC) / (float64(len(text)*(len(text)-1))/25.0)
  fmt.Printf("IC: %f \n", IC)
  return IC
}

func Modulo(a, b int) int {
  temp := a % b
  if temp < 0 {
    return (temp + b)
  }
  return temp
}

func ReplaceChar(s string, pos int, character rune) string {
  newString := s[0:pos-1] + string(character) + s[pos+1:]
  return newString
}

func FiveBest(squareStrings[]string, text string) []string {
  // create the map with the keys the IC value and a bucket containing all strings that have that IC value
  m := make(map[float64][]string)
  for _, squareString := range squareStrings {
    decodedText := PlayfairDecode(text, squareString)

    IC := CalcIC(decodedText)

    m[IC] = append(m[IC], squareString)
  }
  // sort the key
  var keys []float64
  for k := range m {
      keys = append(keys, k)
  }
  sort.Float64s(keys)

  ret := make([]string, 5)
  rem := 5
  for pos:= 0 ; pos <5; pos++  {
    ap := m[keys[pos]]
    if (len(ap) > rem) {
      // just add 1st 5
      for i:=0;i<rem;i++ {
        ret[i]=ap[i]
      }
    } else {
      for i:=0;i<rem;i++ {
        ret[5-rem+i]=ap[i]
      }
      rem -= len(ap)
    }
    pos+=len(ap)-1
  }

  return ret
}
