package monoAlphaticCyphers

import (
	//"fmt"
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

func Modulo(a, b int) int {
	temp := a % b
	if temp < 0 {
		return (temp + b)
	}
	return temp
}
