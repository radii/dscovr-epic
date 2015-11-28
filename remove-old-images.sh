#!/bin/sh

find ~/dscovr -type f -mtime +10 -print0 | xargs -0 rm
