import os
import sys
import json
import urllib
import urllib2
import urlparse
from subprocess import call, Popen, PIPE

if len(sys.argv) < 2 or len(sys.argv) > 3:
    sys.stderr.write("Error: Invalid Arguments\n" +
        "Usage: pre-update.py <repo> [PROJECT-HOME]\n" +
        "E.g. : pre-update.py my-repo /home/user/Workspace\n")
    sys.exit(1)

try:
    USER = os.environ['CIRCLE_USER']
except KeyError:
    sys.stderr.write("Error: CIRCLE_USER has not been sets\n" +
        "Please add `CIRCLE_USER` in your system environment variable")
    sys.exit(1)

TEMPORARY_BRANCH = 'pkg-update'

##############################
# Setting the Repo Directory #
##############################
try:
    WORKSPACE = sys.argv[2]
except IndexError as e:
    try:
        WORKSPACE = os.environ['WORKSPACE']
    except KeyError as e:
        WORKSPACE = os.path.join(os.environ['HOME'], 'Workspace')
REPO = sys.argv[1]
REPO_DIR = os.path.join(WORKSPACE, REPO)

def sh(cmd):
    print("#>>> {}".format(cmd))
    return call(cmd, shell=True)

def main():
    print("""
    =================
    Executing Script:
    =================
    """)
    if os.path.exists(REPO_DIR):
        os.chdir(REPO_DIR)
        sh("git checkout master")
        sh("git pull")
    else:
        os.chdir(WORKSPACE)
        data = {
            'user': USER,
            'repo': REPO,
        }
        sh("git clone git@github.com:{user}/{repo}.git".format(**data))
        os.chdir(REPO_DIR)

    sh("git checkout -B {branch}".format(branch=TEMPORARY_BRANCH))

    sh("bundle update")

    sh("git add Gemfile.lock")

    commit_message = "Auto Commit: Package Update"
    sh("git commit -m '{msg}'".format(msg=commit_message))

    sh("git push -u origin {} --force".format(TEMPORARY_BRANCH))

    sh("git checkout master")

    POST_SCRIPT = os.path.join(os.getcwd(), 'post-update.py')
    sh("at -f {post_script} -v next minute".format(post_script=POST_SCRIPT))

if __name__ == '__main__':
    main()
