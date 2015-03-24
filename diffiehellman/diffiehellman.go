package diffiehellman

//import "strings"

/*
 * Daarvoor neemt zij een a die zij alsvolgt maakt:
 * Ze neemt de titel van een boek. Hierin vervangt zij alle characters van deze titel door hun ASCII-waarde (tussen 32 en 127). Van deze ASCII-waarde trekt zij telkens 32 af, zodat er getallen ontstaan tussen 00 en 95. Deze getallen worden aan elkaar gelijmd tot een groot natuurlijk getal.
 * (%%begin voorbeeld
 * bv: "Pluk van de petteflet" wordt
 * (ascii)
 * [80, 108, 117, 107, 32, 118, 97, 110, 32, 100, 101, 32, 112, 101, 116, 116, 101, 102, 108, 101, 116],
 * (alles -32)
 * [48, 76, 85, 75, 00, 86, 65, 78, 00, 68, 69, 00, 80, 69, 84, 84, 69, 70, 76, 69, 84]
 * (aan elkaar)
 * 487685750086657800686900806984846970766984
 * %%einde voorbeeld)
*/

// SingleNumberToAscii converts a single (two digiti) number to the ASCII character
func SingleNumberToAscii(number uint8) rune {
    
    number += 32
    return rune(number)
    
}

// Convert slices of numbers to ASCII string
func NumbersToAscii(numbers []uint8) string {
    
    var out string
    
    for _,number := range numbers {
        out += string(SingleNumberToAscii(number))
    }
    
    
    return out
    
}