#!/bin/bash

source zimcommon.sh

if [ -f "$TODAY" ]; then
    ./dedupzim.py -i "$TODAY"

    cat "$TODAY" | python ./tohtml.py >"$HOME/Dropbox/todo/today"

    cd $DIR
    git add "$TODAY"
    git commit "$TODAY" -m "cleanup on $(date +%F)"
else
    source zimdaily.sh
fi
