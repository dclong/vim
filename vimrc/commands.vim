
" -------- define some commands ---------
command! ShabangBash :normal! ggi#!/bin/bash<Esc>
command! AppendFileName :call append(line('.'), expand('%:t'))
command! FunScript :normal! Goif [ "$0" == ${BASH_SOURCE[0]} ]; then<Esc>:AppendFileName<CR>| :normal! j$a $@<Esc>>>ofi<Esc>

