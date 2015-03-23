package playfair

import (
	. "github.com/smartystreets/goconvey/convey"
	"testing"
	"math/rand"
	"sort"
)

func TestPlayfair(t *testing.T) {
	Convey("test NewPlayfairSquare", t, func() {
		codeword := "ROBIN"

		square := NewPlayfairSquare(codeword)

		So(square.GetPos('R')[0], ShouldEqual, 0)
		So(square.GetPos('R')[1], ShouldEqual, 0)
		So(square.GetRune(0, 0), ShouldEqual, 'R')

		So(square.GetPos('A')[0], ShouldEqual, 1)
		So(square.GetPos('A')[1], ShouldEqual, 0)
		So(square.GetRune(1, 0), ShouldEqual, 'A')

		So(square.GetPos('Z')[0], ShouldEqual, 4)
		So(square.GetPos('Z')[1], ShouldEqual, 4)
		So(square.GetRune(4, 4), ShouldEqual, 'Z')

	})

	Convey("test Playfair encoding", t, func() {
		codeword := "ROBIN"
		text1 := "TEST"
		text2 := "AA" // this should be encoded as AXAX

		retText1 := Playfair(text1, codeword)
		retText2 := Playfair(text2, codeword)

		So(len(retText1), ShouldEqual, 4)
		So(len(retText2), ShouldEqual, 4)

		So(retText1, ShouldEqual, "YLTU")
		So(retText2, ShouldEqual, "DVDV")

	})
	Convey("test Playfair Decoding", t, func() {
		codeword := "ROBIN"
		text1 := "YL"
		text2 := "DV" // this should be decoded as AXAX

    square := NewPlayfairSquare(codeword)
    retText1 := square.Decrypt(text1)
    retText2 := square.Decrypt(text2)
		So(retText1, ShouldEqual, "TE")
		So(retText2, ShouldEqual, "AX")

		text3 := "TEST"
		encodedText := Playfair(text3, codeword)
		decodedText := PlayfairDecode(encodedText, codeword)
		So(decodedText, ShouldEqual, text3)
	})
}

func TestRandom(t *testing.T) {
	Convey("test permutation", t, func() {
	    rand1 := rand.Perm(10)
	    rand2 := rand.Perm(10)

	    So(rand1, ShouldNotEqual, rand2)

			randomNr1 := rand.Int()
			randomNr2 := rand.Int()

			So(randomNr1, ShouldNotEqual, randomNr2)
	})
}

func TestReplaceChar(t *testing.T) {
	Convey("test ReplaceChar", t, func() {
			text1 := "TEST"
			ReplaceChar(text1, 2, 'X' )
			So(text1, ShouldNotEqual, "TEXT")

	})
}

func TestSort(t *testing.T) {
	Convey("test Sort", t, func() {
		m := make(map[int]string)
		m[1] = "a"
		m[2] = "c"
		m[0] = "b"

		// To store the keys in slice in sorted order
		var keys []int
		for k := range m {
				keys = append(keys, k)
		}
		sort.Ints(keys)

		So(keys[0], ShouldBeLessThan, keys[1] )

	})
}


func TestHillClimb(t *testing.T) {
	Convey("test Best5", t, func() {
		codeWords := []string {"ROBIN", "ROBIN", "ROBIN", "ROBIN", "ROBIN"}
		text := "TTTT"
		FiveBest(codeWords, text)

	})

	Convey("test hillClimb", t, func() {
        //HillClimbCrack("DGDG")
    })
}
