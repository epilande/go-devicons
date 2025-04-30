<div align="center">
  <h1>go-devicons</h1>
</div>

<p align="center">
  <strong>A Go library for mapping files/folders to Nerd Font icons and colors.</strong>
</p>

## ❓ Why?

When building command-line tools or file explorers in Go, displaying appropriate icons can enhance the user experience, providing quick visual cues about file types. `go-devicons` simplifies this by providing a straightforward way to map Nerd Font icon and corresponding color for files and directories, leveraging the comprehensive icon mappings from [nvim-web-devicons](https://github.com/nvim-tree/nvim-web-devicons) project.

This library is useful for enhancing terminal applications, file explorers, or any Go program that needs to display visually distinct file representations.

## 📦 Installation

To use `go-devicons` in your Go project, install it using `go get`:

```sh
go get github.com/epilande/go-devicons
```

## 🎮 Usage

The library provides two main functions to get the icon style:

1.  `IconForPath(path string) icons.Style`: Takes a file system path, determines the file type (regular, directory, symlink) using `os.Lstat`, and returns the best matching style.
2.  `IconForInfo(info os.FileInfo) icons.Style`: Takes an existing `os.FileInfo` object (useful if you've already read directory contents), and returns the best matching style based on the info.

Both functions return an `icons.Style` struct:

```go
// Style holds the suggested icon and hex color for a file/directory.
type Style struct {
	Icon  string
	Color string
}
```

### Basic Example

Here's a simple example demonstrating how to get and print the icon for files in the current directory:

```go
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/epilande/go-devicons"
)

func main() {
	targetDir := "."
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

		// Get the icon style using FileInfo
		fileStyle := devicons.IconForInfo(info)

		// Get the icon style using Path (alternative)
		// path := filepath.Join(targetDir, entry.Name())
		// fileStyle := devicons.IconForPath(path)

		// Print the icon and name (basic, no color)
		fmt.Printf("%s %s %s\n", fileStyle.Icon, entry.Name(), fileStyle.Color)
	}
}
```

> [!TIP]
> The `Color` field in the `Style` struct is a hex string (e.g., `#RRGGBB`). You can use libraries like `lipgloss` or your own terminal coloring methods to apply it.

## 🔌 API Reference

| Function / Type                       | Description                                                                                                                                 |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `IconForPath(path string) Style`      | Returns the `Style` for a given file system path. It calls `os.Lstat` internally to determine if the path is a file, directory, or symlink. |
| `IconForInfo(info os.FileInfo) Style` | Returns the `Style` based on an existing `os.FileInfo`. More efficient if you already have `FileInfo` (e.g., from `os.ReadDir`).            |
| `Style` struct                        | Contains `Icon` (string representing the Nerd Font character) and `Color` (string, hex format `#RRGGBB`).                                   |

## 🌟 Acknowledgements

The icon mappings used in this library are automatically generated from the Lua source files of [nvim-web-devicons](https://github.com/nvim-tree/nvim-web-devicons). Full credit goes to the maintainers and contributors of that project for curating the extensive icon set.
