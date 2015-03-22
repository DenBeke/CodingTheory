package playfair

import (
	. "github.com/smartystreets/goconvey/convey"
	"testing"
	"math/rand"
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

	})
}

func TestRandom(t *testing.T) {
	Convey("test permutation", t, func() {
	    rand1 := rand.Perm(10)
	    rand2 := rand.Perm(10)
	    
	    So(rand1, ShouldNotEqual, rand2)
	})
}

func TestHillClimb(t *testing.T) {
	Convey("test hillClimb", t, func() {
        HillClimbCrack("DGDG") 
    })
}
