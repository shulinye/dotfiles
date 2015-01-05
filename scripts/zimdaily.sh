#!/bin/bash

NOTESDIR="$HOME/Notes"
JOURNALDIR="$HOME/Notes/Journal" #where is this zimwiki journal?
DIR="$JOURNALDIR/$(date +%Y/%m)"
mkdir -p "$DIR"
TODAY="$DIR/$(date +%d).txt"
YESTERDAY="$JOURNALDIR/$(date -d 'yesterday' +%Y/%m/%d.txt)"
TODO="$NOTESDIR/1_-_to-Do.txt"
DAILY="$NOTESDIR/1_-_to-Do/Daily_Tasks.txt"
WEEKLY="$NOTESDIR/1_-_to-Do/Weekly_Tasks.txt"
DoW=1 #Which day of the week do I want to have weekly tasks go to? 1 = Monday, 7 = Sunday (this uses $(date +%u))
TAGS="@journal @diary"

function movetasks(){
    if [ -f "$1" ] ; then
        #Move incomplete tasks from one file to another
        sed -ne '1,/===== Future? =====/{/===== Future? =====/!p}' "$1" | grep "\[ \]\|===\|^[\s]*$" | grep -v "~~.*~~$" >> "$TODAY"
        echo -e "\n\n" >> $TODAY
    fi
}

if [ ! -f "$TODAY" ] ; then

echo -e "Content-Type: text/x-zim-wiki
Wiki-Format: $(zim --version | head -n1)
Creation-Date: $(date +"%FT%T%:z") \n
====== $(date +"%A %d %b %Y") ====== \n
$TAGS \n
==== Tasks ==== \n\n" > "$TODAY"

echo -e "=== FROM TODO ===\n\n" >> "$TODAY"
movetasks "$TODO"

echo -e "=== FROM DAILY ===\n\n" >> "$TODAY"
movetasks "$DAILY"

if [ $(date +%u) = $DoW ] ; then
    echo -e "=== FROM WEEKLY ===\n\n" >> "$TODAY"
    movetasks "$WEEKLY"
fi

echo -e "=== FROM YESTERDAY ===\n\n" >> "$TODAY"
movetasks "$YESTERDAY"
if [ -f "$YESTERDAY" ] ; then
    if [ "$(grep -c '\[ \]' "$YESTERDAY" )" -gt 0 ] ; then
        sed -i -e '/~~/!s/\[ \] /\[x\] ~~/' -e '/~~.*~~/!s/~~.*$/&~~/' "$YESTERDAY"
        #Strike out yesterday's tasks.
        "$HOME/.dotfiles/scripts/dedupzim.py" < "$YESTERDAY" | sponge "$YESTERDAY" #little bit of cleanup
        cd "$JOURNALDIR"
        git add "$YESTERDAY"
        git commit "$YESTERDAY" -m "Moving tasks from $(date -d 'yesterday' +%F) over to $(date +%F)"
    fi
fi

echo -e "==== Tasks Completed ==== \n
==== Diary ==== \n\n" >> "$TODAY"

cat -s "$TODAY" | "$HOME/.dotfiles/scripts/dedupzim.py" | sponge "$TODAY" #This line gets rid of extraneous whitespace and duplicate lines

cd "$DIR"
git add "$TODAY"
git commit "$TODAY" -m "Initial commit: $(date +%F)"
fi
