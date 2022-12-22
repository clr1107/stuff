#!/usr/bin/env bash
USAGE="arxiv.sh <output> <input>"

if [[ "$OSTYPE" == "darwin" ]]; then
	echo "Not yet supporting OSX"
	exit 0
fi

if [ "$#" -ne 2 ]; then
	echo "$USAGE"
	exit 1
fi

tar cf - "$2" -P | pv -s $(du -sb "$2" | awk '{print $1}') | zstd -z -T0 > "$1"
