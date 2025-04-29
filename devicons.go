package devicons

import (
	"os"
	"path/filepath"

	"github.com/epilande/go-devicons/internal/icons"
	"github.com/epilande/go-devicons/internal/mapping"
)

// IconForPath returns the appropriate icon for a given file system path.
// It checks the file's status (directory, symlink, regular file) and name/extension.
func IconForPath(path string) icons.Style {
	info, err := os.Lstat(path)
	name := filepath.Base(path)

	if err != nil {
		isDir := false
		isSymlink := false
		return mapping.LookupStyle(name, isDir, isSymlink)
	}

	isDir := info.IsDir()
	isSymlink := info.Mode()&os.ModeSymlink != 0

	return mapping.LookupStyle(name, isDir, isSymlink)
}

// IconForInfo returns the appropriate icon using existing os.FileInfo.
// Useful when file information has already been retrieved (e.g., during os.ReadDir).
func IconForInfo(info os.FileInfo) icons.Style {
	name := info.Name()
	isDir := info.IsDir()
	isSymlink := info.Mode()&os.ModeSymlink != 0

	return mapping.LookupStyle(name, isDir, isSymlink)
}
