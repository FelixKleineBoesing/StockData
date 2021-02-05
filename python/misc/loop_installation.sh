#!/usr/bin/env bash
dirs=$(ls -d src/*/)
for dir in $dirs;
do
file="$dir"requirements.txt
if [[ -f "$file" ]]; then
    pip3 install -r $file --user
fi
echo $dir;
done