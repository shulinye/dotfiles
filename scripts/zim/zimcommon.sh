#!/bin/bash

source ../dotfiles_venv/bin/activate

HOME="/home/shulinye"
NOTESDIR="$HOME/Notebooks/Notes"
JOURNALDIR="$NOTESDIR/Journal" #where is this zimwiki journal?
DIR="$JOURNALDIR/$(date +%Y/%m)"
mkdir -p "$DIR"
TODAY="$DIR/$(date +%d).txt"
YESTERDAY="$JOURNALDIR/$(date -d 'yesterday' +%Y/%m/%d.txt)"
TODO="$NOTESDIR/1_-_to-Do.txt"
DAILY="$NOTESDIR/1_-_to-Do/Daily_Tasks.txt"
THISWEEK="$DIR/Week_`date +%U`.txt"
DoW=1 #Which day of the week do I want to have weekly tasks go to? 1 = Monday, 7 = Sunday (this uses $(date +%u))

RTMMIRROR="$NOTESDIR/1_-_to-Do/RTM-Mirror.txt"

function movetasks(){
    if [ -f "$1" ] ; then
        #Move incomplete tasks from one file to another
        sed -ne '6,/===== Future? =====\|Tasks Completed/{/===== Future? =====\|Tasks Completed/!p}' "$1" |\
                #Truncate file before Future or Tasks Completed. Start at line 6 to avoid top header
            sed -e 's/^==\(.*\)==$/=\1=/g' |\
                #Reduce the priority of each header
            grep "\[ \]\|==\|^[\s]*$" |\
                #copy undone tasks and headers
            grep -v "~~.*~~$" >> "$2"
                #remove things that are struck through
        echo -e "\n\n" >> "$2"
    fi
}
