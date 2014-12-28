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


function movetasks(){
    if [ -f "$1" ] ; then
        #Move incomplete tasks from one file to another
        grep "\[ \]" "$1" | grep -v "~~$" >> "$TODAY"
        echo -e "\n" >> $TODAY
    fi
}

if [ ! -f "$TODAY" ] ; then

echo "Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: $(date +"%FT%T%:z")

====== $(date +"%A %d %b %Y") ======

=== Tasks ===

" > "$TODAY"

movetasks "$YESTERDAY"
movetasks "$TODO"
movetasks "$DAILY"
if [ $(date +%u) = $DoW ] ; then
    movetasks "$WEEKLY"
fi

echo "=== Tasks Completed ===

=== Diary ===

" >> "$TODAY"
cd "$DIR"
git add "$TODAY"
git commit "$TODAY" -m "Initial commit: $(date +%F)"
fi