package enigma

import (
	"fmt"
	"CodingTheory/rotor"
	"strings"
)

type Enigma interface {
	Encode(text string, rotorPos string) string
	TryClosedPath(invariantChar rune, rotorPos string, k []int) bool
	GetFix(closedPaths [][]int)
	GetFixSpecific(closedPaths [][]int)
}

type EnigmaClass struct {
	reflector Reflector
	plugboard Plugboard
	rotors    [3]rotor.Rotor
}

func (e EnigmaClass) Encode(text string, rotorPos string) string {
	// set the start position of the rotors:
	e.rotors[0].SetOffset(rune(rotorPos[0]))
	e.rotors[1].SetOffset(rune(rotorPos[1]))
	e.rotors[2].SetOffset(rune(rotorPos[2]))

	// clear the text of any whitespace
	r := strings.NewReplacer(" ", "")
	text = r.Replace(text)
	// set all characters to uppercase
	text = strings.ToUpper(text)

	//encode letter per letter
	newText := ""
	for i := 0; i < len(text); i++ {
		working := rune(text[i])
		working = e.plugboard.Plug(working)
		working = e.rotors[0].EncodeRtoL(working)
		working = e.rotors[1].EncodeRtoL(working)
		working = e.rotors[2].EncodeRtoL(working)

		working = e.reflector.Reflect(working)
		working = e.rotors[2].EncodeLtoR(working)
		working = e.rotors[1].EncodeLtoR(working)
		working = e.rotors[0].EncodeLtoR(working)
		working = e.plugboard.Plug(working)
		newText += string(working)

		// click the rotors
		click := true
		for j := 0; j < 3; j++ {
			if click {
				click = e.rotors[j].Click()
			}
		}
	}

	return newText
}

/**
 * Checks if invariantChar doesn't change after going through closedPath
 * in this Enigma (with fixed rotor order and initial setting)
 */
func (e EnigmaClass) TryClosedPath(invariantChar rune, rotorPos string, steps []int) bool {

	inputChar := invariantChar

	for i := 0; i < len(steps); i++ {
		// set the start position of the rotors (for every letter)
		e.rotors[0].SetOffset(rune(rotorPos[0]))
		e.rotors[1].SetOffset(rune(rotorPos[1]))
		e.rotors[2].SetOffset(rune(rotorPos[2]))
		for j := 0; j < steps[i]; j++ {
			// click the rotors enough times up to the needed setting
			click := true
			for j := 0; j < 3; j++ {
				if click {
					click = e.rotors[j].Click()
				}
			}
		}
		//Encode the letter
		working := inputChar
		working = e.rotors[0].EncodeRtoL(working)
		working = e.rotors[1].EncodeRtoL(working)
		working = e.rotors[2].EncodeRtoL(working)

		working = e.reflector.Reflect(working)
		working = e.rotors[2].EncodeLtoR(working)
		working = e.rotors[1].EncodeLtoR(working)
		working = e.rotors[0].EncodeLtoR(working)

		inputChar = working //Continue with the resulting letter

	}
	//Check if the letter is back to the original
	return inputChar == invariantChar

}

/**
 * Finds any k (expressed through the matching initial rotor setting) for which some letter is invariant
 * for all given closed paths. Prints any found setting-leter combination
 */
func (e EnigmaClass) GetFix(closedPaths [][]int) {
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	settings := MakeRotorSettings()
	//Try with each letter (as the letter in the node could be mapped to any letter with the plugboard)
	for i := 0; i < len(alphabet); i++ {
		//Try with each initial rotor setting
		for j := 0; j < 17576; j++ {
			result := true
			//Get the next setting to be tested
			setting := settings.GetNext()
			//Try each closed path
			for k := 0; k < len(closedPaths); k++ {
				thisResult := e.TryClosedPath(rune(alphabet[i]), setting, closedPaths[k])
				if !thisResult {
					result = false
					break //No need to continue if one path doesn't work
				}
			}
			//Only print if it worked for every path
			if result {
				fmt.Printf("hit for %q with setting %q \n", alphabet[i], setting)
			}
		}
	}
}

/**
 * Modified version of the above GetFix, only using one specific rotor setting
 * Only to be used after determining the correct rotor setting
 */
func (e EnigmaClass) GetFixSpecific(closedPaths [][]int) {
	alphabet := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	//Try with each letter
	for i := 0; i < len(alphabet); i++ {
		result := true
		setting := "KSY"
		//Try each closed path
		for k := 0; k < len(closedPaths); k++ {
			thisResult := e.TryClosedPath(rune(alphabet[i]), setting, closedPaths[k])
			if !thisResult {
				result = false
				break
			}
		}
		//Only print if it worked for every path
		if result {
			fmt.Printf("hit for %q with setting %q \n", alphabet[i], setting)
		}
	}
}

func NewEnigma(r [3]rotor.Rotor, refl Reflector, plug Plugboard) Enigma {
	ret := EnigmaClass{rotors: r, reflector: refl, plugboard: plug}
	return ret
}
