#!/bin/sh

export BUTLER_VIRTUALENV=$1
export BUTLER_MANAGEDIR=$2
export BUTLER_SETTINGS=$3

CALLDIR=$(dirname $(readlink -f $0))
export PATH=$PATH:$CALLDIR

BUTLER_NAME=`alfred get settings.BUTLER_NAME`
PROCESS_NAME=alfred-$BUTLER_NAME 
LOCK_FILE=/tmp/$PROCESS_NAME.lock

#/bin/sh $CALLDIR/butler-daemon.sh

nohup /bin/sh $CALLDIR/butler-daemon.sh > /dev/null 2> /dev/null &

