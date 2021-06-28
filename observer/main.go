package main

import (
	"os"

	"github.com/ebi/gsoc-2021/observer/cmd"

	_ "github.com/ebi/gsoc-2021/observer/include"
)

func main() {
	if err := cmd.RootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}
