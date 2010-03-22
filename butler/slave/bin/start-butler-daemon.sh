#!/bin/sh

VIRTUALENV=$1
SETTINGS=$2
CALLDIR=$(dirname $(readlink -f $0))
nohup sh $CALLDIR/butler-daemon.sh "$VIRTUALENV" "$SETTINGS" > /dev/null 2> /dev/null &

