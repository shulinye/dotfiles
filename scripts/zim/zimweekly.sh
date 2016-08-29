#!/bin/bash

source zimcommon.sh

LASTWEEK="$JOURNALDIR/`date +'%Y/%m/Week_%U' -d '7 days ago'`.txt"
WEEKLY="$NOTESDIR/1_-_to-Do/Weekly_Tasks.txt"
TAGS="@Year$(date +%Y) @Month$(date +%m)"
NEXTWEEK="$NOTESDIR/1_-_to-Do/Next_Week.txt"

if [ ! -f "$THISWEEK" ] ; then

echo -e "Content-Type: text/x-zim-wiki
Wiki-Format: $(zim --version | head -n1)
Creation-Date: $(date +"%FT%T%:z") \n
====== Week $(date +"%U, %Y") ====== \n
$TAGS \n
==== Quote ==== \n
$(fortune)\n
==== Tasks ==== \n\n" > "$THISWEEK"

movetasks "$NEXTWEEK" "$THISWEEK"
head -n6 "$NEXTWEEK" | sponge "$NEXTWEEK"

echo -e "=== WEEKLY TASKS ===\n\n" >> "$THISWEEK"
movetasks "$WEEKLY" "$THISWEEK"


if [ -f "$LASTWEEK" ] ; then

    echo -e "=== FROM LAST WEEK (Week $(date +'%U' -d '7 days ago')) ===\n\n" >> "$THISWEEK"
    movetasks "$LASTWEEK" "$THISWEEK"

    if [ "$(grep -c '\[ \]' "$LASTWEEK" )" -gt 0 ] ; then
        sed -i -e '/~~/!s/\[ \] /\[x\] ~~/' -e '/~~.*~~/!s/~~.*$/&~~/' "$LASTWEEK"
        "$HOME/.dotfiles/scripts/zim/dedupzim.py" -i "$LASTWEEK" #little bit of cleanup
        cd "$JOURNALDIR"
        git add "$LASTWEEK"
    fi
fi

"$HOME/.dotfiles/scripts/zim/dedupzim.py" -i "$THISWEEK"

cd $DIR
git add "$THISWEEK"
fi

