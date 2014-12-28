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
    if [ -f "$TODAY" ] ; then
        grep '\[ \]' "$TODAY" | grep -v '~~$'
    fi
}
