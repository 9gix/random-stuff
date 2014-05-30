#!/bin/sh

PROJ_DIR="/home/eugene/tmp"
cd $PROJ_DIR
repo="git@github.com:9gix/random-stuff.git"
proj_name="random-stuff"
remote="origin"
default_branch="master"

if cd ${PROJ_DIR%%/}/$proj_name
then
	git pull $remote $default_branch
else
	git clone $repo $proj_name
	cd $proj_name
fi

git checkout -B bot/bundle-update
git push -u origin bot/bundle-update
git checkout $default_branch


# One more hour check for the test and merge if pass (See post-update.sh)
BUNDLE_MERGER_SCRIPT="/home/eugene/Workspace/random-stuff/script/post-update.sh"
at -f $BUNDLE_MERGER_SCRIPT -v next minute
