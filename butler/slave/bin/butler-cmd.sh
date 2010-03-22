#!/bin/sh

VIRTUALENV=$1
SETTINGS=$2
CALLDIR=$(dirname $(readlink -f $0))

$VIRTUALENV/bin/python $CALLDIR/manage.py butler_$3 --settings=$SETTINGS $4 $5 $6 $7 $8 $9

