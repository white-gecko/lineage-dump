#!/bin/sh

LC_ALL=C
EXPORT=lineage.nt
WIKI_REPO=../lineage_wiki/

MESSAGE="Update LineageOS Device Data"

cd $WIKI_REPO
git pull
cd -
python3 extract.py

git add $EXPORT
git commit -m "$MESSAGE"
