#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

terminals=(
    "gnome-terminal"
    "konsole"
    "xterm"
    "urxvt"
    "rxvt-unicode"
    "st"
    "stterm"
    "alacritty"
    "kitty"
    "wezterm"
    "foot"
    "ghostty"
    "terminator"
    "tilix"
    "xfce4-terminal"
    "mate-terminal"
    "lxterminal"
    "sakura"
    "terminology"
    "qterminal"
    "cool-retro-term"
    "zutty"
    "rio"
    "contour"
    "extraterm"
    "hyper"
    "tabby"
)

# Package name mappings for common differences
declare -A package_names=(
    ["st"]="stterm"
    ["urxvt"]="rxvt-unicode"
    ["cool-retro-term"]="cool-retro-term"
    ["xfce4-terminal"]="xfce4-terminal"
    ["mate-terminal"]="mate-terminal"
)

echo -e "${BOLD}Terminal Availability Check${NC}"
echo -e "${BOLD}===========================${NC}\n"

for term in "${terminals[@]}"; do
    if command -v "$term" &> /dev/null; then
        path=$(which "$term")
        echo -e "${GREEN}✓${NC} ${BOLD}$term${NC} (${BLUE}$path${NC})"
    else
        # Check if package exists
        pkg_name=${package_names[$term]:-$term}
        if apt-cache show "$pkg_name" &>/dev/null 2>&1; then
            echo -e "${RED}✗${NC} ${BOLD}$term${NC} (${YELLOW}package: $pkg_name${NC})"
        else
            echo -e "${RED}✗${NC} ${BOLD}$term${NC}"
        fi
    fi
done