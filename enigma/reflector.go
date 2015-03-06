package enigma

import (
	"log"
)

type Reflector interface {
	Reflect(rune) rune
}

type EnigmaReflector struct {
	mapping map[rune]rune
}

func (e EnigmaReflector) Reflect(r rune) rune {
	return e.mapping[r]
}

func NewReflector(config string) Reflector {
	p := make(map[rune]rune)
	// set the plugboard according to the config string
	for i := 0; i < 26; i++ {
		p[rune(i+65)] = rune(config[i])
	}

	// check that it is a 1 on 1 mapping
	for i := int('A'); i <= int('M'); i++ {
		val1 := p[rune(i)]
		val2 := p[val1]

		if val2 != rune(i) {
			log.Fatal("Reflector: You did not give a correct config string, %q and %q should be a 1 on 1 mapping ", rune(val1), rune(val2))
		}
	}

	pb := EnigmaReflector{mapping: p}
	return pb

}
