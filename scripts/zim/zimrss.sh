#!/bin/bash

. ./zimcommon.sh

function replacezimfile() {
    echo -e "$(head -n6 $1) \n $(./zimrss.py "${@:2}")" | sponge "$1"
}

echo "Goodreads!"
replacezimfile "$NOTESDIR/Book_recommendations/To-Read(Goodreads).txt" "goodreads" "to-read"
replacezimfile "$NOTESDIR/Currently-Reading.txt" "goodreads" "currently-reading" --prefix \*

echo "RTM->Mirror!"
replacezimfile "$NOTESDIR/1_-_to-Do/RTM-Mirror.txt" "rtm" "all"
