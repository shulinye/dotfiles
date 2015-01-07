#!/bin/bash

NOTESDIR="$HOME/Notes"
JOURNALDIR="$HOME/Notes/Journal" #where is this zimwiki journal?
DIR="$JOURNALDIR/$(date +%Y/%m)"
mkdir -p "$DIR"
TODAY="$DIR/$(date +%d).txt"

if [ -f "$TODAY" ]; then
    ./dedupzim.py < "$TODAY" | sponge "$TODAY"

    cd $DIR
    git add "$TODAY"
    git commit "$TODAY" -m 'cleanup on $(date +%F)'
fi
