alias yolo="sudo"
alias :q="exit"
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

function tasks()
{
    TODAY="$HOME/Notes/Journal/$(date +%Y/%m/%d.txt)"
    THISMONTH="$HOME/Notes/Journal/$(date +%Y/%m.txt)"
    if [ -f "$TODAY" ] ; then
        echo -e "${BOLD}Today's tasks${NONE}"
        grep '\[ \]' "$TODAY" | grep -v '~~.*~~$'
        echo -e "\n"
    fi

    if [ -f "$THISMONTH" ] ; then
        echo -e "${BOLD}This month's tasks${NONE}"
        grep '\[ \]' "$THISMONTH" | grep -v '~~.*~~$' | grep -v 'Week [0-9]'
        echo -e "\n"
    fi


    #RTM tasks - test the site first so I don't hang if, say, my internet is not working
    if wget -q --spider rememberthemilk.com ; then
        echo -e "${BOLD}RTM tasks${NONE}"
        "$HOME/.dotfiles/scripts/zimrss.py" "rtm"
    else
        echo -e "${BOLD}Internet down, cannot check RTM. Using local mirror${NONE}"
        grep '\[ \]' "$HOME/Notes/1_-_to-Do/RTM-Mirror.txt" | grep -v '~~.*~~$'
    fi
}
