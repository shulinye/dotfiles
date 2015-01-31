#!/bin/bash

source zimcommon.sh

TAGS="@journal @diary"

function movetasks(){
    if [ -f "$1" ] ; then
        #Move incomplete tasks from one file to another
        sed -ne '6,/===== Future? =====\|Tasks Completed/{/===== Future? =====\|Tasks Completed/!p}' "$1" |\
                #Truncate file before Future or Tasks Completed. Start at line 6 to avoid top header
            sed -e 's/^==\(.*\)==$/=\1=/g' |\
                #Reduce the priority of each header
            grep "\[ \]\|===\|^[\s]*$" |\
                #copy undone tasks and headers
            grep -v "~~.*~~$" >> "$TODAY"
                #remove things that are struck through
        echo -e "\n\n" >> $TODAY
    fi
}

if [ ! -f "$TODAY" ] ; then

echo -e "Content-Type: text/x-zim-wiki
Wiki-Format: $(zim --version | head -n1)
Creation-Date: $(date +"%FT%T%:z") \n
====== $(date +"%A %d %b %Y") ====== \n
$TAGS \n
==== Quote ==== \n
$(fortune)\n
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


cat -s "$TODAY" |\
        #Remove extraneous whitespace
    "$HOME/.dotfiles/scripts/dedupzim.py" |\
        #Remove duplicate lines
    sponge "$TODAY"

cd "$DIR"
git add "$TODAY"
git commit "$TODAY" -m "Initial commit: $(date +%F)"
fi
