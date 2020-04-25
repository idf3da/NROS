#!/bin/bash
mkdir ./ci/public
python ./api_backend/test.py
OUTPUT=$(cat ./ci/public/api_test.txt)
echo "$OUTPUT"
SUB='OK'
if [[ "$OUTPUT" == *"$SUB"* ]]
then
    anybadge --label=api --value=passing --file=./ci/public/api_test.svg passing=green failing=red
else
    anybadge --label=api --value=failing --file=./ci/public/api_test.svg passing=green failing=red
fi