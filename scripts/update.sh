#!/bin/bash
HOUR=$(date +%H)
FROM_HOUR=1
TO_HOUR=6
TODAY=$(date +"%Y-%m-%d")

for i in "$@"
do
    case $i in
        -f|--force)
            UPDATE=True
            ;;
        *)
            echo "Unknown args $i"
            ;;
    esac
done

if [ ! $TERMINAL_ID ]; then
    echo "Set TERMINAL_ID in .bash_rc"
    exit 1
fi

if (( $FROM_HOUR <= 10#$HOUR && 10#$HOUR < $TO_HOUR )); then 
    UPDATE=True
fi

if [ $UPDATE ]; then
    rsync -rvL --delete-after --progress --rsh 'ssh -p 7626' videoad@allsol.ru:sites/videoAd/server/media/terminals/$TERMINAL_ID/$TODAY/ /home/terminal/videoad_data/$TODAY/
fi
