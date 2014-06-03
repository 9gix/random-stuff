"""
Get the latest test status of `package-update` branch from the CI.

if `package-update` branch has passed all the test:
    merge the `package-update` brach into `master` branch
    push the `master` branch

Requirements:
    Environment variable: (put these variable in your bashrc file)
    - CIRCLE_USER
    - CIRCLE_TOKEN

syntax:
    python post-update.py <repo-name>

Usage:
    python post-update.py my-repo

Developer Note:
- GitPython: https://pythonhosted.org/GitPython/0.3.1/tutorial.html
"""

import os
import git
import sys
import json
import urllib
import urllib2
import urlparse

if len(sys.argv) < 2 or len(sys.argv) > 3:
    sys.stderr.write("Error: Invalid Arguments\n" +
        "Usage: post-update.py <repo> [PROJECT-HOME]\n" +
        "E.g. : post-update.py my-repo /home/user/Workspace\n")
    sys.exit(1)


REPO = sys.argv[1]
USER = os.getenv('CIRCLE_USER')
TOKEN = os.getenv('CIRCLE_TOKEN')
TEMPORARY_BRANCH = 'pkg-update'

try:
    WORKSPACE = sys.argv[2]
except IndexError as e:
    try:
        WORKSPACE = os.environ['WORKSPACE']
    except KeyError as e:
        WORKSPACE = os.path.join(os.environ['HOME'], 'Workspace')

# create project directory unless exists
if not os.path.exists(WORKSPACE):
    os.makedirs(PROJECT_HOME)

def is_circle_ci_test_pass(user, repo, branch, token):
    data = {
        'user': user,
        'repo': repo,
        'branch': branch,
        'token': token,
        'limit': 1,
    }
    circle_ci_resource = 'https://circleci.com/api/v1/'
    target_path = "project/{user}/{repo}/tree/{branch}?" \
            "circle-token={token}&limit={limit}".format(
                    **data)
    url = urlparse.urljoin(circle_ci_resource, target_path)
    headers = {'Accept': 'application/json'}
    req = urllib2.Request(url, headers=headers)
    resp = urllib2.urlopen(req)
    data = json.load(resp)

    try:
        last_build = data[0]
    except IndexError as e:
        print("No last build found")
        return False

    if last_build.get('status') is 'success':
        return True
    else:
        print("Bundle Update Fail the test, don't merge to master")
        return False

def is_test_pass(user, repo, branch, token):
    return is_circle_ci_test_pass(user, repo, branch, token)

def main():
    pkg_update_branch = TEMPORARY_BRANCH
    path = os.path.join(WORKSPACE, REPO)
    repo = git.Repo(path)
    if is_test_pass(USER, REPO, pkg_update_branch, TOKEN):
        repo.git.checkout('head', b='master')
        git.Index.from_tree(repo, 'base', 'HEAD', pkg_update_branch)

if __name__ == '__main__':
    main()
