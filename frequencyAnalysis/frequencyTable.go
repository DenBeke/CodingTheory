package frequencyAnalysis

import ("strings"
  "fmt")

type FrequencyTable struct {
  frequencyMap map[rune]float32
}

func NewFrequencyTable(text string) FrequencyTable {
  m := make(map[rune]float32)
  absoluteMap := make(map[rune]int)
  // clear the text of any whitespace
  r := strings.NewReplacer(" ", "")
  text = r.Replace(text)
  // set all characters to uppercase
  text = strings.ToUpper(text)

  for i:=0; i<len(text); i++ {
    absoluteMap[rune(text[i])] += 1
  }
  fmt.Printf("%d", len(text))
  // calculate frequency
  for i:= 65; i<91; i++ {
    m[rune(i)] = float32(absoluteMap[rune(i)])/float32(len(text))
  }
  ret := FrequencyTable{frequencyMap: m}
  return ret
}
