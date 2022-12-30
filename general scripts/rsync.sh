#!/usr/bin/env bash
# rsync.sh [opts]

if [ "$#" -eq 0 ] || [ "$1" == "-h" ]; then
	echo "Usage: rsync.sh [opts] <src> <dst>"
	echo "For Linux FS use opts: -a"
	echo "For reduced FS use opts: -r --size-only"
	echo "For deleting, use: --delete-delay --delete-excluded"
	echo "To disable compression use: --no-z"
	exit 0
fi

# a = rlptgoD
OPTS="-v --no-i-r --info=progress2 --stats --human-readable --partial -z -@=2"

CMD="rsync $OPTS $@"
echo -e "Execute the following command? (y/n)\n\n$CMD\n"
read EX

case $EX in
    [yY] ) echo "Executing...";$CMD;
        exit;;
    [nN] ) echo "Exiting...";
        exit;;
    * ) echo "Input y/n";
        exit;;
esac
