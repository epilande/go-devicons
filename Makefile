SCRIPT = lua2go.py
LUA_SRC_DIR = ../nvim-web-devicons/lua/nvim-web-devicons/default/
GO_DEST_DIR = internal/icons

.PHONY: icons all

all: icons

# Target to generate the Go icon files
icons: $(SCRIPT)
	@echo "🚀 Generating Go icons from $(LUA_SRC_DIR)..."
	@python3 $(SCRIPT) $(LUA_SRC_DIR) -o $(GO_DEST_DIR)
	@echo "✅ Go icons generated in $(GO_DEST_DIR)"

