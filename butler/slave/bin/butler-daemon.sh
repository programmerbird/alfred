#!/bin/sh

VIRTUALENV=$1
SETTINGS=$2
CALLDIR=$(dirname $(readlink -f $0))
ALFRED="$CALLDIR/butler-cmd.sh $VIRTUALENV $SETTINGS"

BUTLER_NAME=`$ALFRED get settings.BUTLER_NAME`
PROCESS_NAME=alfred-$BUTLER_NAME 
LOCK_FILE=/tmp/$PROCESS_NAME.lock

if [ -f $LOCK_FILE ] ; then
	# the lock file already exists, so what to do?
	if [ "$(ps -p `cat /tmp/$PROCESS_NAME.lock` | wc -l)" -gt 1 ]; then
		# process is still running
		echo "$0: quit at start: lingering process `cat $LOCK_FILE`"
		exit 0
	else
		# process not running, but lock file not deleted?
		echo "$0: orphan lock file warning. Lock file deleted."
		rm $LOCK_FILE
	fi
fi

echo $$ > $LOCK_FILE


APP=`$ALFRED fetch`
while [ -n "$APP" ]; do
	$APP "$1"
	APP=`$ALFRED fetch`
done


rm -f $LOCK_FILE

