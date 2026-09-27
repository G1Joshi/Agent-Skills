---
name: vim
description: Expert Vim assistance covering modal editing, .vimrc configuration, registers, macros, search/replace, and plugin management via vim-plug. Use when editing text efficiently in terminal environments, writing Vimscript, recording macros, or configuring core Vim settings.
---

# Vim

Vim is the universal text editor installed on every UNIX system. While Neovim innovates, Vim focuses on backward compatibility and stability.

## When to Use

- **Universal Server & System Editing**: Editing system configs, scripts, and code on any Unix/Linux server without installing external software.
- **Modal Text Manipulation**: Composing text transformations with operator-motion grammar (`dap`, `ci"`, `gUiw`).
- **Headless Macro Automation**: Recording and replaying repetitive editing operations across hundreds of lines (`qa`, `@a`).
- **Git Commit & Merge Editing**: Fast interactive editing for commit messages, interactive rebases, and diff conflict resolution.

## Quick Start

### 1. Minimal ~/.vimrc

```vim
syntax on
set number
set relativenumber
set tabstop=2
set shiftwidth=2
set expandtab
set hlsearch
set incsearch
set clipboard=unnamed

let mapleader = " "
nnoremap <leader>w :w<CR>
nnoremap <leader>q :q<CR>
```

### 2. Core Editing Commands

- `i` / `a`: Insert mode (before / after cursor)
- `ci"`: Change inside quotes
- `da{`: Delete around curly braces
- `:%s/foo/bar/g`: Replace all occurrences of foo with bar in file
- `.` : Repeat last modification

## Core Concepts

### Modern Production Vimrc (`~/.vimrc`)

Configuring sensible defaults, plugin manager, and code navigation:

```vim
" ~/.vimrc
set nocompatible
filetype plugin indent on
syntax on

" General settings
set number
set relativenumber
set expandtab
set shiftwidth = 2
set tabstop = 2
set autoindent
set smartindent
set hlsearch
set incsearch
set ignorecase
set smartcase
set hidden
set backspace=indent,eol,start
set updatetime=300
set clipboard=unnamed

" Leader key mapping
let mapleader = " "

" Fast split navigation
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Clear search highlight
nnoremap <leader>h :nohlsearch<CR>
```

### Essential Text Objects & Grammar

Combining operators (`d`, `c`, `y`, `v`) with text objects and motions:

```text
ci"      - Change inside double quotes ("foo" -> "")
di(      - Delete inside parentheses
yap      - Yank (copy) around paragraph
gUiw     - Convert inner word to UPPERCASE
dt,      - Delete from cursor until comma
.        - Repeat last change immediately
```

### Macro Recording & Execution

Automating repetitive tabular data transformations:

```text
1. Press `qa` to start recording macro into register 'a'
2. Perform text editing steps (e.g. `0iconst <Esc>A = true;<Esc>j`)
3. Press `q` to finish recording
4. Replay macro on current line: `@a`
5. Replay macro 50 times across lines: `50@a`
6. Run macro on visual selection: `:'<,'>normal @a`
```

## Common Patterns

### Macro Recording and Bulk Execution

**Problem**: Perform repetitive multi-step edits across multiple lines.  
**Solution**: Record keystrokes into register `q`.

1. Place cursor at target start position.
2. Press `qq` to start recording to register `q`.
3. Perform editing sequence (e.g. `I" <Esc> A",<Esc> j ^`).
4. Press `q` to stop recording.
5. Replay with `@q`, or run across 50 lines: `50@q`.

### Plugin Management with vim-plug

**Problem**: Install and organize Vim plugins without manual path manipulation.  
**Solution**: Use `vim-plug`.

```vim
call plug#begin('~/.vim/plugged')
Plug 'tpope/vim-sensible'
Plug 'tpope/vim-fugitive'
Plug 'preservim/nerdtree'
call plug#end()
```

Run `:PlugInstall` inside Vim to install.

## Best Practices (2026)

- **Do** master modal navigation (`h`, `j`, `k`, `l`, `w`, `b`, `e`) and avoid reaching for arrow keys.
- **Do** leverage Text Objects (`ciw`, `da(`, `yi{`) to edit structured code blocks with minimal keystrokes.
- **Do** use the dot command (`.`) to repeat recent text transformations across similar lines.
- **Do** enable `set hidden` so buffers can stay open in the background without forcing immediate saves.
- **Don't** install hundreds of heavy legacy VimScript plugins; transition to Neovim Lua if a rich IDE experience is required.
- **Don't** leave swap files (`.swp`) lingering; configure `set noswapfile` or set a dedicated swap directory.
- **Don't** use synchronous external calls in `~/.vimrc` that cause noticeable startup delay on remote machines.

## Troubleshooting

| Error / Symptom                                        | Cause                                     | Solution                                                                           |
| ------------------------------------------------------ | ----------------------------------------- | ---------------------------------------------------------------------------------- |
| System clipboard copy fails (`"+y` does nothing)       | Vim compiled without `+clipboard` support | Install `vim-gtk3` (Ubuntu) or `macvim` / `neovim` with clipboard support enabled. |
| Arrow keys insert `A`, `B`, `C`, `D` characters        | Running in strict Vi compatible mode      | Add `set nocompatible` at top of `~/.vimrc`.                                       |
| Trailing whitespace highlighting persists after search | Highlight search remained active          | Press `:nohlsearch` or bind `<leader>h :nohlsearch<CR>`.                           |

## References

- [Vim Documentation](https://www.vim.org/docs.php)
