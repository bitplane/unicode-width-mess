# Unicode width tests

Mapping out the mess that is Unicode character widths. Brute force the entire range,
print a char, check wcswidth against the cursor position.

Run in your favourite terminal, add your results to ./results and send a pull request.

## Results

| Terminal              | Mismatches | Date       | OS    | Distro      | Hash     |
|-----------------------|------------|------------|-------|-------------|----------|
| kitty                 | 268        | 2025-06-09 | linux | ubuntu24_04 | 53087cd6 |
| konsole               | 274        | 2025-06-09 | linux | ubuntu24_04 | d589539d |
| alacritty             | 445        | 2025-06-09 | linux | ubuntu24_04 | dbd66d5a |
| gnome-terminal-server | 459        | 2025-06-09 | linux | ubuntu24_04 | a81cbceb |
| sakura                | 459        | 2025-06-10 | linux | ubuntu24_04 | b23a7ad7 |
| foot                  | 529        | 2025-06-09 | linux | ubuntu24_04 | 3b3ce53c |
| zutty                 | 531        | 2025-06-09 | linux | ubuntu24_04 | 7dd629e1 |
| xterm                 | 531        | 2025-06-09 | linux | ubuntu24_04 | 8b335a2c |
| st                    | 531        | 2025-06-09 | linux | ubuntu24_04 | 9a8f94c3 |
| urxvt                 | 531        | 2025-06-09 | linux | ubuntu24_04 | unknown  |
| ghostty               | 559        | 2025-06-09 | linux | ubuntu24_04 | 9697fc54 |
| tmux                  | 566        | 2025-06-09 | linux | ubuntu24_04 | fb3a1384 |
| screen                | 1711       | 2025-06-09 | linux | ubuntu24_04 | 975a4a08 |
| terminology           | 6781       | 2025-06-09 | linux | ubuntu24_04 | 77aa2a39 |
