# Unicode width tests

Mapping out the mess that is Unicode character widths. Brute force the entire range,
print a char, check wcswidth against the cursor position.

Run in your favourite terminal, add your results to ./results and send a pull request.

## results

💩 | terminal
---|----------
268 | kitty
274 | konsole
445 | alacritty
459 | gnome-terminal-server
529 | foot
531 | st
531 | urxvt
531 | xterm
531 | zutty
559 | ghostty
566 | tmux
1711 | screen
6781 | terminology
