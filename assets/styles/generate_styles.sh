#!/bin/bash

styles=(
    base16 base16.dark base16.light base16.monokai base16.monokai.dark 
    base16.monokai.light base16.solarized base16.solarized.dark base16.solarized.light 
    bw colorful github github.dark github.light gruvbox gruvbox.dark 
    gruvbox.light igorpro magritte molokai monokai monokai.sublime pastie 
    thankful_eyes tulip
)

for style in "${styles[@]}"; do
    rougify style "$style" > "assets/css/$style.css"
    echo "Generated assets/css/$style.css"
done