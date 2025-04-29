package main

import (
	"fmt"
	"log"
	"os"

	"github.com/charmbracelet/lipgloss"
	"github.com/epilande/go-devicons"
)

func main() {
	targetDir := "."
	if len(os.Args) > 1 {
		targetDir = os.Args[1]
	}

	entries, err := os.ReadDir(targetDir)
	if err != nil {
		log.Fatalf("Error reading directory '%s': %v\n", targetDir, err)
	}

	fmt.Printf("Listing contents of '%s':\n", targetDir)

	for _, entry := range entries {
		info, err := entry.Info()
		if err != nil {
			fmt.Printf("? %s (Error getting info: %v)\n", entry.Name(), err)
			continue
		}

		fileStyle := devicons.IconForInfo(info)

		lipglossStyle := lipgloss.NewStyle().Foreground(lipgloss.Color(fileStyle.Color))

		coloredIcon := lipglossStyle.Render(fileStyle.Icon)

		separator := " "
		if fileStyle.Icon == "" {
			separator = ""
		}
		fmt.Printf("%s%s%s\n", coloredIcon, separator, entry.Name())
	}
}
