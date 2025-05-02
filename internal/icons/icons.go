package icons

// Style holds the suggested icon and hex color for a file/directory.
// Color is in "#RRGGBB" format or empty if no specific color is defined.
type Style struct {
	Icon  string
	Color string
}

var (
	DefaultStyle = Style{Icon: "", Color: "#ABB2BF"}
	DirStyle     = Style{Icon: "", Color: "#61AFEF"}
	SymlinkStyle = Style{Icon: "", Color: "#56B6C2"}
)
