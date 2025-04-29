package mapping

import (
	"path/filepath"
	"strings"

	"github.com/epilande/go-devicons/internal/icons"
)

// LookupStyle finds the best matching Style for a given file/directory name.
// It prioritizes symlinks, then exact directory/filename matches,
// then directory name "extensions", then file extensions, and finally falls back to defaults.
func LookupStyle(name string, isDir, isSymlink bool) icons.Style {
	if isSymlink {
		return icons.SymlinkStyle
	}

	if isDir {
		if style, ok := icons.IconsByFilename[name]; ok {
			return style
		}

		ext := getExtension(name)
		if ext != "" {
			if style, ok := icons.IconsByFileExtension[ext]; ok {
				return style
			}
		}

		return icons.DirStyle
	}

	if style, ok := icons.IconsByFilename[name]; ok {
		return style
	}

	ext := getExtension(name)
	if ext != "" {
		if style, ok := icons.IconsByFileExtension[ext]; ok {
			return style
		}
	}

	return icons.DefaultStyle
}

// getExtension extracts the extension from a filename.
// Handles dotfiles (e.g., ".bashrc" -> "bashrc") and files without extensions
// (e.g., "Makefile" -> "makefile").
func getExtension(name string) string {
	if name == "" {
		return ""
	}

	if name[0] == '.' && !strings.Contains(name[1:], ".") {
		if len(name) > 1 {
			return strings.ToLower(name[1:])
		}
		return ""
	}

	ext := filepath.Ext(name)

	if ext == "" {
		if !strings.Contains(name, ".") {
			return strings.ToLower(name)
		}
		return ""
	}

	return strings.ToLower(ext[1:])
}
