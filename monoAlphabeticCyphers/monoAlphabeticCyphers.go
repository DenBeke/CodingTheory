package monoAlphaticCyphers

import (
	"fmt"
	"strings"
)

func Rot(n int, text string) string {
	// clear the text of any whitespace
	r := strings.NewReplacer(" ", "")
	text = r.Replace(text)
	// set all characters to uppercase
	text = strings.ToUpper(text)

	newText := ""
	for i := 0; i < len(text); i++ {
		// add n to int value of the rune
		working := rune(text[i])
		working = rune(Modulo(int(working-65)+n, 26) + 65)
		newText += string(working)
	}
	return newText
}

func Atbash(text string) string {
	// setup an AtbashMap:
	atbashMap := make(map[rune]rune)
	for j := 0; j < 26; j++ {
		atbashMap[rune(65+j)] = rune(65 + 25 - j)
	}

	// clear the text of any whitespace
	r := strings.NewReplacer(" ", "")
	text = r.Replace(text)
	// set all characters to uppercase
	text = strings.ToUpper(text)

	newText := ""
	for i := 0; i < len(text); i++ {
		// add n to int value of the rune
		working := rune(text[i])
		working = atbashMap[working]
		newText += string(working)
	}
	return newText
}

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

func NewPlayfairSquare(codeWord string) PlayfairSquare {

	var s [5][5]rune
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
		for j := 0; j < len(fullCode); j++ {
			if rune(fullCode[j]) == rune(i) {
				seen = true
				break
			}
		}
		if !seen {
			fullCode += string(i)
		}
	}

	if len(fullCode) != 25 {
		fmt.Printf("Problem with CodeWord \n")
	}
	// setup square and positionMap
	for i := 0; i < 5; i++ {
		for j := 0; j < 5; j++ {
			s[i][j] = rune(fullCode[5*(i-1)+j])
			p[rune(fullCode[5*(i-1)+j])] = [2]int{i, j}
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
	}

	// if the number of letters is Odd, add an X to the end
	if (len(newText) % 2) != 0 {
		newText += "X"
	}

	retText := ""
	// take digrams from the text.
	for i := 1; i < len(newText); i += 2 {
		letter1 := rune(newText[i])
		letter2 := rune(newText[i+1])
		pos1 := square.GetPos(letter1)
		pos2 := square.GetPos(letter2)

		var newLetter1 rune
		var newLetter2 rune
		if pos1[1] == pos2[1] {
			// zelfde rij:
			// kolom+1
			newLetter1 = square.GetRune(pos1[0], (pos1[1]+1)%5)
			newLetter2 = square.GetRune(pos2[0], (pos2[1]+1)%5)
		} else {
			if pos1[0] == pos2[0] {
				// zelfde kolom: rij+1
				newLetter1 = square.GetRune((pos1[0]+1)%5, pos1[1])
				newLetter2 = square.GetRune((pos2[0]+1)%5, pos2[1])
			} else {
				// andere rij en kolom
				// neem hoekpunten van de rechthoek
				newLetter1 = square.GetRune(pos1[0], pos2[1])
				newLetter2 = square.GetRune(pos2[0], pos1[1])
			}
		}
		retText += string(newLetter1)
		retText += string(newLetter2)
	}

	return retText
}

func Modulo(a, b int) int {
	temp := a % b
	if temp < 0 {
		return (temp + b)
	}
	return temp
}
