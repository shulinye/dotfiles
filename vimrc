"Use vim settings, rather then vi settings (much better!)
" This must be first, because it changes other options as a side effect.
set nocompatible

" Oh right, puting my name on things can be useful
let g:C_AuthorName      = 'Shulin Ye'
let g:C_Email           = 'nightshadequeen@gmail.com'

"""Use mouse if available
if has('mouse')
    set mouse=a
    set ttymouse=xterm2
endif

set showmode " always show what mode we're currently editing in

" Editor layout {{{
set termencoding=utf-8
set encoding=utf-8
set lazyredraw " don't update the display while executing macros
set laststatus=2 " tell VIM to always put a status line in, even
" if there is only one window
set cmdheight=2 " use a status bar that is 2 rows high
set scrolloff=3 " Try to keep 3 lines above/below the current line in view for context.
set viminfo+=!,h " give me viminfo, please
set more                " more:  page on extended output
set nomodeline
filetype plugin indent on
set cursorline
" }}}


"""Text things (defaults){{{
set tabstop=4 " a tab is four spaces
set softtabstop=4 " when hitting <BS>, pretend like a tab is removed, even if spaces
set expandtab " expand tabs by default (overloadable per file type later)
set shiftwidth=4 " number of spaces to use for autoindenting
set shiftround " use multiple of shiftwidth when indenting with '<' and '>'
set backspace=indent,eol,start " allow backspacing over everything in insert mode
set autoindent " always set autoindenting on
set copyindent " copy the previous indentation on autoindenting
set number " always show line numbers
set ruler "ensures each window contains a status line
set showmatch " set show matching parenthesis
set incsearch "vim will search for text as you type
set ignorecase
set smartcase " ignore case if search pattern is all lowercase,
" case-sensitive otherwise
set smarttab " insert tabs on the start of a line according to
" shiftwidth, not tabstop
""" }}}

"""Text things (specific to filetype) {{{

" in human-language files, automatically format everything at 72 chars:
autocmd FileType mail,human set formatoptions+=t textwidth=72
" for C-like programming, have automatic indentation:
autocmd FileType c,cpp,slang set cindent
" for actual C (not C++) programming where comments have explicit end characters, if starting a new line in the middle of a comment automatically insert the comment leader characters:
autocmd FileType c set formatoptions+=ro
" for Perl programming, have things in braces indenting themselves:
autocmd FileType perl set smartindent
" for CSS, also have things in braces indented:
autocmd FileType css set smartindent
" for HTML, generally format text, but if a long line has been created leave it alone when editing:
autocmd FileType html set formatoptions+=tl
" for both CSS and HTML, use genuine tab characters for indentation, to make files a few bytes smaller:
autocmd FileType html,css set noexpandtab tabstop=2
" in makefiles, don't expand tabs to spaces, since actual tab characters are needed, and have indentation at 8 chars to be sure that all indents are tabs (despite the mappings later):
autocmd FileType make set noexpandtab shiftwidth=8
" }}}

set pastetoggle=<F2> " when in insert mode, press <F2> to go to
" paste mode, where you can paste mass data
" that won't be autoindented

" Flag problematic whitespace (trailing spaces, spaces before tabs).
highlight BadWhitespace term=standout ctermbg=red guibg=red
match BadWhitespace /[^* \t]\zs\s\+$\| \+\ze\t/

""" History, Autocomplete, and Backups {{{
set history=1000 " remember more commands and search history
set undolevels=1000 " use many muchos levels of undo
set wildmode=list:longest,full "cmdline completion (for filenames, help topics, option names)
set wildignore=*~,#*#,*.sw?,*.o,*.class,*.java.html,*.cgi.html,*.html.html,.viminfo,*.pdf,*.mp3

set backup
" Write swap files to the temp directory
if has("win32") || has("win64")
    set directory=$TMP
    set backupdir=$TMP
else
    set directory=/tmp
    set backupdir=~/.vim/backup
end
" }}}

""" Spelling !!! {{{
set spellsuggest=3  "suggest better spelling
set spelllang=en    "set language
set dictionary+=/usr/dict/words
"""}}}

set title " change the terminal's title

set guifont=Consolas:h9
set background=dark
set autoread                  " watch for file changes
set noerrorbells              " No error bells please

if has('syntax') && (&t_Co > 2)
  syntax on
endif

" Allow usage of hidden buffers
set hidden

" Set current working directory based on current file.
autocmd BufEnter * lcd %:p:h


" Map forward/backward buffer navigation.
map <C-right> <ESC>:bn<CR>
map <C-left> <ESC>:bp<CR>

" Because I'm a stupid human who makes typos
:command WQ wq
:command Wq wq
:command W w
:command Q q
