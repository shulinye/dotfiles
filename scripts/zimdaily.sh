#!/bin/bash

source zimcommon.sh

TAGS="@journal @diary @Year$(date +%Y)"

if [ ! -f "$TODAY" ] ; then

echo -e "Content-Type: text/x-zim-wiki
Wiki-Format: $(zim --version | head -n1)
Creation-Date: $(date +"%FT%T%:z") \n
====== $(date +"%A %d %b %Y") ====== \n
Week $(date +%V)\n
$TAGS \n
==== Quote ==== \n
$(fortune)\n
==== Tasks ==== \n\n" > "$TODAY"

echo -e "=== FROM TODO ===\n\n" >> "$TODAY"
movetasks "$TODO" "$TODAY"

echo -e "=== FROM DAILY ===\n\n" >> "$TODAY"
movetasks "$DAILY" "$TODAY"

if [ $(date +%u) = $DoW ] ; then
    echo -e "=== FROM WEEKLY ===\n\n" >> "$TODAY"
    movetasks "$WEEKLY" "$TODAY"
fi

echo -e "=== FROM YESTERDAY ===\n\n" >> "$TODAY"
movetasks "$YESTERDAY" "$TODAY"
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

ln -sf "$TODAY" "/home/shulinye/Dropbox/todo/today"
