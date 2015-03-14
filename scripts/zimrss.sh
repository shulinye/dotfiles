#!/bin/bash

. ./zimcommon.sh


function replacezimfile() {
    echo "$(head $1) $(./zimrss.py "${@:2}")" | sponge "$1"
}

replacezimfile "$NOTESDIR/Book_recommendations/To-Read(Goodreads).txt" "goodreads" "to-read"
