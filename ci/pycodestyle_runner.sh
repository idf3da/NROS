#!/bin/bash
mkdir public
pycodestyle ../ --count -qq &> ./public/pycodestyle.txt
OUTPUT=$(cat ./public/pycodestyle.txt)
echo "$OUTPUT"
if [[ "$OUTPUT" == '' ]]
then
    anybadge --label=pep8 --value=passing --file=public/pycodestyle.svg passing=green failing=red
else
    anybadge --label=pep8 --value=failing --file=public/pycodestyle.svg passing=green failing=red
fi
exit 1
