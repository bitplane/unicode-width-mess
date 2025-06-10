# Unicode width tests

Mapping out the mess that is Unicode character widths. Brute force the entire range,
print a char, check wcswidth against the cursor position.

Run in your favourite terminal, add your results to ./results and send a pull request.

## Results

| Terminal              | Mismatches | Date       | OS    | Distro      | Hash     |
|-----------------------|------------|------------|-------|-------------|----------|
| qterminal             | 241        | 2025-06-10 | linux | ubuntu24_04 | 73cae2ee |
| kitty                 | 268        | 2025-06-09 | linux | ubuntu24_04 | 53087cd6 |
| konsole               | 274        | 2025-06-09 | linux | ubuntu24_04 | d589539d |
| alacritty             | 445        | 2025-06-09 | linux | ubuntu24_04 | dbd66d5a |
| sakura                | 459        | 2025-06-10 | linux | ubuntu24_04 | b23a7ad7 |
| gnome-terminal-server | 459        | 2025-06-09 | linux | ubuntu24_04 | a81cbceb |
| cool-retro-term       | 529        | 2025-06-10 | linux | ubuntu24_04 | 5aa39d41 |
| foot                  | 529        | 2025-06-09 | linux | ubuntu24_04 | 3b3ce53c |
| st                    | 531        | 2025-06-09 | linux | ubuntu24_04 | 9a8f94c3 |
| xterm                 | 531        | 2025-06-09 | linux | ubuntu24_04 | 8b335a2c |
| zutty                 | 531        | 2025-06-09 | linux | ubuntu24_04 | 7dd629e1 |
| urxvt                 | 531        | 2025-06-09 | linux | ubuntu24_04 | unknown  |
| ghostty               | 559        | 2025-06-09 | linux | ubuntu24_04 | 9697fc54 |
| tmux                  | 566        | 2025-06-09 | linux | ubuntu24_04 | fb3a1384 |
| screen                | 1711       | 2025-06-09 | linux | ubuntu24_04 | 975a4a08 |
| terminology           | 6781       | 2025-06-09 | linux | ubuntu24_04 | 77aa2a39 |
