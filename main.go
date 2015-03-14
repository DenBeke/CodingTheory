package main

import "os"
import "fmt"
import "github.com/DenBeke/CodingTheory/enigma"

func main() {

	if len(os.Args) == 1 {
		println("Usage:", os.Args[0], "input.json")
		return
	}

	enigma_config, err := enigma.ReadConfig(os.Args[1])

	if err != nil {
		println("Error:", err)

	}

	fmt.Println(enigma_config)
	e := enigma_config.CreateEnigma()
	encoded := e.Encode("TEST", "AAA")
	fmt.Printf("%q \n", encoded)
	fmt.Printf("Finished encoding \n")
}
