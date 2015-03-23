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
