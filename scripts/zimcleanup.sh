#!/bin/bash

source zimcommon.sh

if [ -f "$TODAY" ]; then
    ./dedupzim.py < "$TODAY" | sponge "$TODAY"

    cd $DIR
    git add "$TODAY"
    git commit "$TODAY" -m "cleanup on $(date +%F)"
fi
