#!/bin/bash

curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1v2bYKnGlnwQG9KIf1VhXCCkPvO8P3Gbz" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1v2bYKnGlnwQG9KIf1VhXCCkPvO8P3Gbz" -o resources.tar.gz
tar -zxvf resources.tar.gz
rm resources.tar.gz

echo Download finished.
