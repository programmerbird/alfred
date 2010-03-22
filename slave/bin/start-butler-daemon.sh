#!/bin/sh

SETTINGS=$1
CALLDIR=$(dirname $(readlink -f $0))
nohup sh $CALLDIR/butler-daemon.sh "$SETTINGS" > /dev/null 2> /dev/null &

