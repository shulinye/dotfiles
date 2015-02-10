#!/bin/bash

source zimcommon.sh

THISMONTH="$DIR.txt"
LASTMONTH="$JOURNALDIR/`date +'%Y/%m.txt' -d 'last month'`"
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

cd $DIR
git add "$THISMONTH"
git commit "$THISMONTH" -m "Initial commit: $(date +'%B %Y')"

fi

