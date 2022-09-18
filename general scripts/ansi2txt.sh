#!/bin/bash

INPUT="$(< /dev/stdin)"
echo "$INPUT" | sed -r "s/\x1B\[(([0-9]{1,2})?(;)?([0-9]{1,2})?)?[m,K,H,f,J]//g"
