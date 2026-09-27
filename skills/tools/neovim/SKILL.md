---
name: neovim
description: Expert Neovim assistance covering Lua configuration, native LSP client, Treesitter syntax highlighting, and plugin management via lazy.nvim. Use when configuring Neovim, writing init.lua, setting up LSP keymaps, managing plugins, or optimizing editor startup performance.
---

# Neovim

Neovim is the future of Vim. v0.11 (2025) brings built-in completion, enhanced LSP, and mature Tree-sitter integration.

## When to Use

- **Modern Lua-Based Editor Setup**: Configuring a high-performance, modular development environment using `init.lua` and Lazy.nvim.
- **LSP & Tree-sitter Code Navigation**: Utilizing Native LSP client, Tree-sitter AST parsing, and Mason package manager.
- **Fuzzy Finding & Buffer Management**: Navigating repositories rapidly using Telescope, Fzf-lua, and Harpoon.
- **Terminal & Remote Development**: Editing code seamlessly over SSH sessions, Docker containers, and headless servers.

## Quick Start

### 1. Minimal init.lua Structure

```lua
-- ~/.config/nvim/init.lua
vim.g.mapleader = " "
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.tabstop = 2
vim.opt.shiftwidth = 2
vim.opt.expandtab = true
vim.opt.termguicolors = true

-- Bootstrap lazy.nvim plugin manager
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },
  { "neovim/nvim-lspconfig" },
  { "nvim-telescope/telescope.nvim", dependencies = { "nvim-lua/plenary.nvim" } },
})
```

### 2. Verify Health

```bash
nvim +checkhealth
```

## Core Concepts

### Modern Modular Configuration (`init.lua` & Lazy.nvim)

Setting up Lazy.nvim package manager with modular plugin specifications in `~/.config/nvim/init.lua`:

```lua
-- ~/.config/nvim/init.lua
vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

-- Core editor options
local opt = vim.opt
opt.number = true
opt.relativenumber = true
opt.expandtab = true
opt.shiftwidth = 2
opt.tabstop = 2
opt.smartindent = true
opt.termguicolors = true
opt.updatetime = 250
opt.signcolumn = "yes"

-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- Configure plugins
require("lazy").setup({
  { "nvim-treesitter/nvim-treesitter", build = ":TSUpdate" },
  { "neovim/nvim-lspconfig" },
  { "williamboman/mason.nvim", config = true },
  { "williamboman/mason-lspconfig.nvim" },
  { "hrsh7th/nvim-cmp", dependencies = { "hrsh7th/cmp-nvim-lsp", "L3MON4D3/LuaSnip" } },
  { "nvim-telescope/telescope.nvim", dependencies = { "nvim-lua/plenary.nvim" } },
  { "catppuccin/nvim", name = "catppuccin", priority = 1000, config = function() vim.cmd.colorscheme("catppuccin-mocha") end },
})
```

### Native LSP & Tree-sitter Integration

Configuring language servers, keymaps, and diagnostics:

```lua
-- ~/.config/nvim/after/plugin/lsp.lua
require("mason").setup()
require("mason-lspconfig").setup({
  ensure_installed = { "ts_ls", "pyright", "gopls", "rust_analyzer", "lua_ls" }
})

local lspconfig = require("lspconfig")
local capabilities = require("cmp_nvim_lsp").default_capabilities()

local on_attach = function(client, bufnr)
  local map = function(keys, func, desc)
    vim.keymap.set("n", keys, func, { buffer = bufnr, desc = "LSP: " .. desc })
  end

  map("gd", vim.lsp.buf.definition, "Goto Definition")
  map("gr", vim.lsp.buf.references, "Goto References")
  map("K", vim.lsp.buf.hover, "Hover Documentation")
  map("<leader>rn", vim.lsp.buf.rename, "Rename Symbol")
  map("<leader>ca", vim.lsp.buf.code_action, "Code Action")
  map("<leader>d", vim.diagnostic.open_float, "Show Diagnostics")
end

-- Setup Go language server
lspconfig.gopls.setup({
  capabilities = capabilities,
  on_attach = on_attach,
  settings = {
    gopls = {
      analyses = { unusedparams = true },
      staticcheck = true,
    }
  }
})
```

### Telescope & Harpoon Workflow

Configuring fuzzy finding across files, symbols, and live grepping:

```lua
-- ~/.config/nvim/after/plugin/telescope.lua
local builtin = require("telescope.builtin")
vim.keymap.set("n", "<leader>ff", builtin.find_files, { desc = "Find Files" })
vim.keymap.set("n", "<leader>fg", builtin.live_grep, { desc = "Live Grep" })
vim.keymap.set("n", "<leader>fb", builtin.buffers, { desc = "Find Buffers" })
vim.keymap.set("n", "<leader>fh", builtin.help_tags, { desc = "Help Tags" })
```

## Common Patterns

### Built-in LSP Configuration

**Problem**: Need language server autocompletion, diagnostics, and definition navigation without heavy external IDE layers.  
**Solution**: Configure servers using `nvim-lspconfig` and standard diagnostic keybindings.

```lua
-- lua/plugins/lsp.lua
local lspconfig = require("lspconfig")

local on_attach = function(client, bufnr)
  local map = function(keys, func, desc)
    vim.keymap.set("n", keys, func, { buffer = bufnr, desc = "LSP: " .. desc })
  end
  map("gd", vim.lsp.buf.definition, "Goto Definition")
  map("K", vim.lsp.buf.hover, "Hover Documentation")
  map("<leader>rn", vim.lsp.buf.rename, "Rename Symbol")
  map("<leader>ca", vim.lsp.buf.code_action, "Code Action")
end

lspconfig.ts_ls.setup({ on_attach = on_attach })
lspconfig.pyright.setup({ on_attach = on_attach })
lspconfig.rust_analyzer.setup({ on_attach = on_attach })
```

### Telescope Fuzzy Finding

**Problem**: Need rapid project file searching, live grep across repository, and buffer navigation.  
**Solution**: Bind Telescope commands to leader hotkeys.

```lua
local builtin = require("telescope.builtin")
vim.keymap.set("n", "<leader>ff", builtin.find_files, { desc = "Find Files" })
vim.keymap.set("n", "<leader>fg", builtin.live_grep, { desc = "Live Grep" })
vim.keymap.set("n", "<leader>fb", builtin.buffers, { desc = "Find Buffers" })
```

## Best Practices (2026)

- **Do** pin plugin dependencies to git release tags or lockfiles (`lazy-lock.json`) to prevent breaking updates.
- **Do** leverage Tree-sitter for syntax highlighting, indentation, and incremental AST code selection.
- **Do** set `updatetime = 250` for responsive diagnostic floats and git gutter refreshes.
- **Do** use `vim.keymap.set` with explicit `desc` attributes to support `which-key.nvim` keymap discovery.
- **Don't** install monolithic legacy VimScript plugins when native Lua alternatives exist.
- **Don't** execute synchronous `io.popen` calls in `init.lua` that stall editor startup time.
- **Don't** commit `lazy-lock.json` merge conflicts without running `:Lazy restore`.

## Troubleshooting

| Error / Symptom                               | Cause                                                              | Solution                                                                                                               |
| --------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `module 'lazy' not found`                     | Plugin manager clone failed or RTP path incorrect                  | Run `git clone --filter=blob:none https://github.com/folke/lazy.nvim.git ~/.local/share/nvim/lazy/lazy.nvim` manually. |
| Treesitter parser compilation failure         | Missing C compiler (`cc`, `clang`, or `gcc`)                       | Install build essentials: `brew install gcc` (macOS) or `apt install build-essential` (Linux).                         |
| LSP `Spawning language server failed: ENOENT` | Language server binary (e.g. `pyright`, `gopls`) is not in `$PATH` | Install server via Mason (`:MasonInstall pyright`) or host package manager.                                            |

## References

- [Neovim Documentation](https://neovim.io/doc/)
