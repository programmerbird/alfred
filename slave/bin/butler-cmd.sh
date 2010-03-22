#!/bin/sh

BASEDIR=$1
SETTINGS=$2

$BASEDIR/env/bin/python $BASEDIR/manage.py butler_$3 --settings=$SETTINGS $4 $5 $6 $7 $8 $9

