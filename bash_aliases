#!/usr/bin/bash
alias yolo="sudo"
alias :q="exit"
alias :wq="exit"
alias wq="exit"

alias j="fasd_cd -d"

function mkdate()
{
    currentdate=$(date +%F)
    if [ ! -d "$currentdate" ]; then
        mkdir -p "$currentdate"
    fi
    cd "$currentdate"
}

function auxpdflatex()
{
    echo "${1%.tex}.pdf"
    echo $pwd
}

function goto()
{
    file="$(f -l $1 | tail -n1)"
    echo "$file"
    cd "$(dirname $file)"
}

function tasks()
{
    TODAY="$HOME/Dropbox/Notes/Journal/$(date +%Y/%m/%d.txt)"
    THISMONTH="$HOME/Dropbox/Journal/$(date +%Y/%m.txt)"
    if [ -f "$TODAY" ] ; then
        echo -e "${BOLD}Today's tasks - $(date +'%d %b %y') ${NONE}"
        grep '\[ \]' "$TODAY" | grep -v '~~.*~~$'
        echo -e "\n"
    fi

    if [ -f "$THISMONTH" ] ; then
        echo -e "${BOLD}This month's tasks - $(date +'%b %Y')${NONE}"
        grep '\[ \]' "$THISMONTH" | grep -v '~~.*~~$' | grep -v 'Week [0-9]\+'
        echo -e "\n"
    fi

    #RTM tasks - test the site first so I don't hang if, say, my internet is not working
    if wget -q --spider rememberthemilk.com ; then
        echo -e "${BOLD}RTM tasks${NONE}"
        "$HOME/.dotfiles/scripts/zim/zimrss.py" "rtm" "all"
    else
        echo -e "${BOLD}Internet down, cannot check RTM. Using local mirror${NONE}"
        grep '\[ \]' "$HOME/Notes/1_-_to-Do/RTM-Mirror.txt" | grep -v '~~.*~~$'
    fi
}
