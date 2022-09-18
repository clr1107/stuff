#!/bin/bash

INPUT="$(< /dev/stdin)"
echo "$INPUT" | sed -e 's/\r$//'
