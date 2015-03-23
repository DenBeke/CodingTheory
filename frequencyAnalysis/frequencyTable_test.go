package frequencyAnalysis

import (
	. "github.com/smartystreets/goconvey/convey"
	"testing"
)

func TestFrequencyTable(t *testing.T) {
	Convey("[FrequencyAnalysis] basis test frequencyTable constructor", t, func() {
		table := NewFrequencyTable("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

		So(table.frequencyMap['A'], ShouldEqual, float32(1.0/26.0))
	})
	Convey("[FrequencyAnalysis] test frequencyTable constructor", t, func() {
		text := "Rabbits are little creatures with long ears and puffy tails and they move their nose up and down in an adorable way They eat the most orange vegetables in our world and they reproduce more than any human ever has"
		table := NewFrequencyTable(text)
		So(table.frequencyMap['A'], ShouldEqual, float32(20.0/float32(173)))
	})

}
