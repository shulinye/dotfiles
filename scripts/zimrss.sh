#!/bin/bash

. ./zimcommon.sh

function replacezimfile() {
    echo -e "$(head -n7 $1) \n $(./zimrss.py "${@:2}")" | sponge "$1"
}

replacezimfile "$NOTESDIR/Book_recommendations/To-Read(Goodreads).txt" "goodreads" "type=to-read"

replacezimfile "$NOTESDIR/Currently-Reading.txt" "goodreads" "type=currently-reading" "prefix=*"

replacezimfile "$NOTESDIR/1_-_to-Do/RTM-Mirror.txt" "rtm" "type=all"
