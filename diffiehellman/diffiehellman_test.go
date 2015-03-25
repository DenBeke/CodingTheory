package diffiehellman

import (
	_ "fmt"
	. "github.com/smartystreets/goconvey/convey"
	"math/big"
	_ "runtime"
	"testing"
)

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

func TestNumbersToAscii(t *testing.T) {
	Convey("test NumbersToAscii", t, func() {

		title_numbers := []uint8{48, 76, 85, 75, 00, 86, 65, 78, 00, 68, 69, 00, 80, 69, 84, 84, 69, 70, 76, 69, 84}
		title := NumbersToAscii(title_numbers)

		So("Pluk van de petteflet", ShouldEqual, title)
	})
}

func TestPrimeFactors(t *testing.T) {
	Convey("test FindPrimeFactors", t, func() {

		pf5 := []uint64{5}
		pf6 := []uint64{2, 3}
		pf10 := []uint64{2, 5}
		pf20 := []uint64{2, 2, 5}
		pf60 := []uint64{2, 2, 3, 5}

		So(pf5, ShouldResemble, FindPrimeFactors(big.NewInt(5)))
		So(pf6, ShouldResemble, FindPrimeFactors(big.NewInt(6)))
		So(pf10, ShouldResemble, FindPrimeFactors(big.NewInt(10)))
		So(pf20, ShouldResemble, FindPrimeFactors(big.NewInt(20)))
		So(pf60, ShouldResemble, FindPrimeFactors(big.NewInt(60)))
	})
}

func TestDiffieHellman(t *testing.T) {

	/*
	   Convey("test DiffieHellman", t, func() {

	       runtime.GOMAXPROCS(runtime.NumCPU())

	       g := big.NewInt(0)
	       y := big.NewInt(0)
	       p := big.NewInt(0)

	       g.SetString("8754324567890876543245678908765432456789", 10)
	       y.SetString("93965208631426420710108237044685554466463776793445", 10)
	       p.SetString("97067553992624667459897809313680908020593207653741", 10)

	       IndexCalculus(g, y, p)


	   })
	*/

}
