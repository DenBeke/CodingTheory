package diffiehellman

//import "strings"
import "math/big"

//import "math"
import "fmt"
import "log"
import "strconv"
import "regexp"
import "runtime"

//import "sync"
//import "runtime"

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

func IntInSlice(a uint64, list []uint64) bool {
	for _, b := range list {
		if b == a {
			return true
		}
	}
	return false
}

// SingleNumberToAscii converts a single (two digiti) number to the ASCII character
func SingleNumberToAscii(number uint8) rune {

	number += 32
	return rune(number)

}

// Convert slices of numbers to ASCII string
func NumbersToAscii(numbers []uint8) string {

	var out string

	for _, number := range numbers {
		out += string(SingleNumberToAscii(number))
	}

	return out

}



// FindPrimeFactors returns slice of prime factors of the given number
func FindPrimeFactors(n *big.Int) (factors []uint64) {

	var d int64 = 2
	var temp = big.NewInt(0)

	for n.Cmp(big.NewInt(1)) == 1 {
		for temp.Mod(n, big.NewInt(d)).Int64() == 0 {
			factors = append(factors, uint64(d))
			//n /= d
			n.Div(n, big.NewInt(d))
		}
		d += 1

		if temp.Mul(big.NewInt(d), big.NewInt(d)).Cmp(n) == 1 {
			if n.Cmp(big.NewInt(1)) == 1 {
				factors = append(factors, n.Uint64())
			}
			break
		}

	}

	return factors
}

type Ki struct {
	k       uint64
	factors []uint64
}

type empty struct{}
type semaphore chan empty

// IndexCalculus of  a = log_g A (mod p)
func IndexCalculus(g *big.Int, y *big.Int, p *big.Int) (u *big.Int) {

	//var s []byte // set of small primes
	s := []uint64{2, 3, 5, 7, 11}
	results := []Ki{}
	//wg := sync.WaitGroup{}
	//semaphore := make(semaphore, runtime.NumCPU())

	// search numbers k_i so g^(k_i) (mod p) in S
	for k := uint64(1); true; k++ {

		//wg.Add(1)
		//semaphore <- empty{}

		// check if prime factors from g^(k_i) (mod p) are in S
		func() {

			//defer wg.Done()

			temp := big.NewInt(0)
			temp.Exp(g, big.NewInt(int64(k)), p).Mod(temp, p)

			hasFactors := true

			fmt.Println(temp)

			primeFactors := FindPrimeFactors(temp)

			fmt.Println(primeFactors)

			for _, i := range primeFactors {
				if !IntInSlice(i, s) {
					hasFactors = false
					break
				}
			}

			if hasFactors {
				results = append(results, Ki{k, primeFactors})
				//fmt.Println("Result!")
				fmt.Println(results)
			}

			//<- semaphore

		}()

		return

		if k == 18446744073709551615 {
			// that's enough!
			break
		}

	}

	//wg.Wait()

	return u
}


func FindUsefulStrings(a1 string, p1 string) {

	runtime.GOMAXPROCS(runtime.NumCPU()*2)

	regex := regexp.MustCompile(`^([a-zA-Z0-9]*[[:space:]]?)*[\.]?$`)

	_ = regex

	a := big.NewInt(0)
	a.SetString(a1, 10)

	p := big.NewInt(0)
	p.SetString(p1, 10) // p-1

	semaphore := make(semaphore, runtime.NumCPU()*2)
	var it uint64 = 0

	for {

		semaphore <- empty{}
		it++

		//a.Add(a, p)

		if it % 1000000 == 0 {
			log.Println(it)
		}

		go func (iteration uint64){

			num := big.NewInt(0)
			new_p := big.NewInt(0)

			num.Set(a)
			num.Add(num, new_p.Mul(big.NewInt(int64(iteration)), p))


			s := []uint8{}

			for i,d := range num.String() {

				if i%2 == 1 && len(s) != 0 {
					i,_ := strconv.ParseInt(string(d), 10, 64)
					s[len(s)-1] = s[len(s)-1]*10 + uint8(i)

				} else {
					i,_ := strconv.ParseInt(string(d), 10, 64)
					s = append(s, uint8(i))
				}
			}


			if regex.MatchString(NumbersToAscii(s)) {
				fmt.Println(NumbersToAscii(s))
			}

			<- semaphore

		}(it)

	}

}



