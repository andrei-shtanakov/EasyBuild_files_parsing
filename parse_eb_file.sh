#!/bin/bash

while read line; do
  # Check if the line starts with "* [x]" or "* [ ]"
  if [[ $line =~ ^\*\ \[x\].* ]] || [[ $line =~ ^\*\ \[\ ].* ]]; then
    # Use parameter expansion to remove the leading "* [x] " or "* [ ] "
    line="${line#* [x] }"
    line="${line#* [ ] }"

    # Use parameter expansion to extract the path (starts after "$CFGS/")
    path="${line#*$CFGS/}"

    # Use parameter expansion to extract the module (starts after " (module: ")
    module="${path#* (module: }"
    module="${module%)*}"

    # The rest of the line is the path without the module information
    path="${path% (module:*}"

    # Print the extracted information
    echo "Checkmark: ${line:2:3}"
    echo "Path: $path"
    echo "Module: $module"
  fi
done < "$1"
