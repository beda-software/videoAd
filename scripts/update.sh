#!/bin/bash
HOUR=$(date +%H)
FROM_HOUR=1
TO_HOUR=6
TERMINAL_ID=1
TODAY=$(date +"%Y-%m-%d")

if (( $FROM_HOUR <= 10#$HOUR && 10#$HOUR < $TO_HOUR )); then 
    rsync -rvL --delete-after --progress --rsh 'ssh -p 7626' videoad@allsol.ru:sites/videoAd/server/media/terminals/$TERMINAL_ID/$TODAY/ /home/terminal/videoad_data/
fi
