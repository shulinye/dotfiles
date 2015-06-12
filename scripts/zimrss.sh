#!/bin/bash

. ./zimcommon.sh

function replacezimfile() {
    echo "$(head -n7 $1) $(./zimrss.py "${@:2}")" | sponge "$1"
}

replacezimfile "$NOTESDIR/Book_recommendations/To-Read(Goodreads).txt" "goodreads" "to-read"

replacezimfile "$NOTESDIR/Currently-Reading.txt" "goodreads" "currently-reading"
