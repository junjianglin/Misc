".vimrc  - startup file for Vim

syntax on
set nu
set mouse=a
"set ai    " auto indent
"set si	  " smart indent
filetype plugin indent on
set tabstop=4  " the width of a Tab is set to 4
set shiftwidth=4 " indents will have a width of 4
set softtabstop=4 "sets the number of columns for a TAB
set expandtab
set laststatus=2 " show the current status


function! InsertStatuslineColor(mode)
  if a:mode == 'i'
    hi statusline guibg=Cyan ctermfg=6 guifg=Black ctermbg=0
  elseif a:mode == 'r'
    hi statusline guibg=Purple ctermfg=3 guifg=Black ctermbg=0
  else
    hi statusline guibg=DarkRed ctermfg=2 guifg=Black ctermbg=0
  endif
endfunction

au InsertEnter * call InsertStatuslineColor(v:insertmode)
au InsertLeave * hi statusline guibg=Purple ctermfg=DarkGreen guifg=White ctermbg=0

" default the statusline to green when entering Vim
hi statusline guibg=DarkGrey ctermfg=LightGreen  guifg=White ctermbg=0

" Formats the statusline
set statusline=
set statusline+=\ %t\                                "File
set statusline+=\ %y\                                  "FileType
set statusline+=\ %{''.(&fenc!=''?&fenc:&enc).''}      "Encoding
set statusline+=\ %{(&bomb?\",BOM\":\"\")}\            "Encoding2
set statusline+=\ %{&ff}\                              "FileFormat (dos/unix..) 
set statusline+=\ %{&spelllang}\  "Spellanguage & Highlight on?
set statusline+=\ Buf:%n                                  "buffernr
set statusline+=\ %=\ Line:%l/%L\ (%03p%%)\             "Rownumber/total (%)
set statusline+=\ Col:%03c\                            "Colnr
set statusline+=\ %m%r%w\ %P\ \                      "Modified? Readonly? Top/bot.

"" Puts in the current git status
"    if count(g:pathogen_disabled, 'Fugitive') < 1   
"        set statusline+=%{fugitive#statusline()}
"    endif
"
"" Puts in syntastic warnings
"    if count(g:pathogen_disabled, 'Syntastic') < 1  
"        set statusline+=%#warningmsg#
"        set statusline+=%{SyntasticStatuslineFlag()}
"        set statusline+=%*
"    endif

