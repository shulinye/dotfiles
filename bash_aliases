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

    wget -q --spider rememberthemilk.com

    if [ $? -eq 0 ]; then
        echo -e "${BOLD}RTM tasks${NONE}"
        "$HOME/.dotfiles/scripts/zimrss.py" "rtm"
    else
        echo "Internet down, cannot check RTM"
    fi
}
