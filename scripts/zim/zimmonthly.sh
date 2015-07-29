#!/bin/bash

source zimcommon.sh

THISMONTH="$DIR.txt"
LASTMONTH="$JOURNALDIR/`date +'%Y/%m.txt' -d 'last month'`"
MONTHLY="$NOTESDIR/1_-_to-Do/Monthly_Tasks.txt"
TAGS="@Year$(date +%Y)"
if [ ! -f "$THISMONTH" ] ; then

echo -e "Content-Type: text/x-zim-wiki
Wiki-Format: $(zim --version | head -n1)
Creation-Date: $(date +"%FT%T%:z") \n
====== $(date +"%B %Y") ====== \n
$TAGS \n
==== Quote ==== \n
$(fortune)\n
==== Tasks ==== \n\n" > "$THISMONTH"


echo -e "=== FROM LAST MONTH ($(date +'%B %Y' -d 'last month')) ===\n\n" >> "$THISMONTH"
movetasks "$LASTMONTH" "$THISMONTH"

if [ -f "$LASTMONTH" ] ; then
    if [ "$(grep -c '\[ \]' "$LASTMONTH" )" -gt 0 ] ; then
        sed -i -e '/~~/!s/\[ \] /\[x\] ~~/' -e '/~~.*~~/!s/~~.*$/&~~/' "$LASTMONTH"
        #Strike out yesterday's tasks.
        "$HOME/.dotfiles/scripts/zim/dedupzim.py" -i "$LASTMONTH" #little bit of cleanup
        cd "$JOURNALDIR"
        git add "$LASTMONTH"
        git commit "$LASTMONTH" -m "Moving tasks from $(date -d 'last month' +'%B %Y') over to $(date +'%B %Y')"
    fi
fi


echo -e "=== MONTHLY TASKS ===\n\n" >> "$THISMONTH"
movetasks "$MONTHLY" "$THISMONTH"

"$HOME/.dotfiles/scripts/zim/dedupzim.py" -i "$THISMONTH"

cd $DIR
git add "$THISMONTH"
git commit "$THISMONTH" -m "Initial commit: $(date +'%B %Y')"

fi

