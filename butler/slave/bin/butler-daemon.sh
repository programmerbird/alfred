#!/bin/sh

BUTLER_NAME=`alfred get settings.BUTLER_NAME`
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

APP=`alfred fetch`
while [ -n "$APP" ]; do
	alfred status proc
	$APP 
	sleep 1
	APP=`alfred fetch`
done


rm -f $LOCK_FILE

