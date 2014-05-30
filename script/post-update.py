import urllib
import urllib2
import urlparse
import os
import json

TOKEN = os.getenv('CIRCLE_TOKEN')
API_URL = "https://circleci.com/api/v1/"
USER = '9gix'
REPO = 'random-stuff'
BRANCH = 'bot%2Fbundle-update'
data = {
    'user': USER,
    'repo': REPO,
    'branch': BRANCH,
    'token': TOKEN,
    'limit': 1,
}

target_path = "project/{user}/{repo}/tree/{branch}?" \
        "circle-token={token}&limit={limit}".format(**data)

# url: https://circleci.com/api/v1/project/:user/:repo/tree/:branch?circle-token=:token
url = urlparse.urljoin(API_URL, target_path)

headers = {'Accept': 'application/json'}
req = urllib2.Request(url, headers=headers)
resp = urllib2.urlopen(req)

def merge(vcs_rev, target_branch='master'):
    # Execute the Git command to pull and merge to master
    pass

data = json.load(resp)
try:
    last_build = data[0]
except IndexError as e:
    print("No last build")
    exit(1)
else:
    if last_build.get('status', False) is 'success':
        vcs_rev = last_build.get('vcs_revision', '')
        target_branch = "master"
        merge(vcs_rev, target_branch)
    else:
        raise Exception("Bundle Update Fail the test, don't merge to master")


