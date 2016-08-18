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

echo -e "=== RTM ===\n\n" >> "$TODAY"
if wget -q --spider rememberthemilk.com; then
    echo -e "$(head -n8 $RTMMIRROR) \n $(./zimrss.py "rtm" "all")" | sponge "$RTMMIRROR"
else
    echo -e "Internet down, from mirror"
fi
if [ -f "$RTMMIRROR" ] ; then
    grep "$(date +'%d %b %y')" "$RTMMIRROR" >> "$TODAY"
fi

echo -e "=== FROM DAILY ===\n\n" >> "$TODAY"
movetasks "$DAILY" "$TODAY"

if [ "$(date +%u)" = "$DoW" ] ; then
    echo -e "=== FROM THIS WEEK ===\n\n" >> "$TODAY"
    movetasks "$THISWEEK" "$TODAY"
fi

echo -e "=== FROM YESTERDAY ===\n\n" >> "$TODAY"
movetasks "$YESTERDAY" "$TODAY"
if [ -f "$YESTERDAY" ] ; then
    if [ "$(grep -c '\[ \]' "$YESTERDAY" )" -gt 0 ] ; then
        sed -i -e '/~~/!s/\[ \] /\[x\] ~~/' -e '/~~.*~~/!s/~~.*$/&~~/' "$YESTERDAY"
        #Strike out yesterday's tasks.
        "./dedupzim.py" -i "$YESTERDAY" #little bit of cleanup
        cd "$JOURNALDIR" &&
        git add "$YESTERDAY" &&
        git commit "$YESTERDAY" -m "Moving tasks from $(date -d 'yesterday' +%F) over to $(date +%F)"
    fi
fi

echo -e "==== Tasks Completed ==== \n
==== Diary ==== \n\n" >> "$TODAY"

"$HOME/.dotfiles/scripts/zim/dedupzim.py" -i "$TODAY"

cd "$DIR" || exit
git add "$TODAY"
git commit "$TODAY" -m "Initial commit: $(date +%F)"
fi

mkdir -p "$HOME/Dropbox/todo"
cat "$TODAY" | python "$HOME/.dotfiles/scripts/zim/tohtml.py" > "$HOME/Dropbox/todo/today"
