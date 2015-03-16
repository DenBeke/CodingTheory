package monoAlphaticCyphers

import (
	. "github.com/smartystreets/goconvey/convey"
	"testing"
)

func TestRot(t *testing.T) {
	Convey("simple rot test", t, func() {
		// test rot function
		text1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		solText := Rot(1, text1)
		So(solText, ShouldEqual, "BCDEFGHIJKLMNOPQRSTUVWXYZA")
	})

	Convey("caesar cypher test", t, func() {
		// this is a rot13 function
		text1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		solText := Rot(1, text1)
		So(solText, ShouldEqual, "BCDEFGHIJKLMNOPQRSTUVWXYZA")
	})

}

func TestAtbash(t *testing.T) {
	Convey("simple atbash test", t, func() {
		// test rot function
		text1 := "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		solText := Atbash(text1)
		So(solText, ShouldEqual, "ZYXWVUTSRQPONMLKJIHGFEDCBA")
	})

	Convey("serious test of Atbash", t, func() {
		// lorem ipsum text
		text1 := "Lorem ipsum dolor sit amet"
		solText := Atbash(text1)
		So(solText, ShouldEqual, "OLIVNRKHFNWLOLIHRGZNVG")

	})
}

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
}
