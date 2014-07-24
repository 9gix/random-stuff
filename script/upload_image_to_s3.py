import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto


BUCKET = ''
ACCESS_KEY = ""
SECRET_KEY = ""
PATH = 'images'

conn = S3Connection(ACCESS_KEY, SECRET_KEY)

try:
    bucket = conn.create_bucket(BUCKET)
except boto.exception.S3CreateError:
    bucket = conn.get_bucket(BUCKET)

key = Key(bucket)
results = []

for root, dirs, filenames in os.walk(PATH):
    data = {
        'directory': root,
        'images': []
    }
    for filename in sorted(filenames):
        fileExt = os.path.splitext(filename)[1]
        if fileExt == '.jpg' and not filename.startswith('.'):
            filepath = os.path.join(root, filename)
            keypath = os.path.join(os.path.split(root)[0], filename)
            key.key = keypath
            if not key.exists():
                key.set_contents_from_filename(filepath)
                key.set_acl('public-read')
            url = key.generate_url(expires_in=0, query_auth=False)
            image = {
                'url': url,
                'id': int(filename.split()[0][0])
            }
            data['images'].append(image)
            print(image)

    if data['images']:
        results.append(data)

import pprint

with open('result.txt', 'w') as outfile:
    pp = pprint.PrettyPrinter(indent=4)
    text = pp.pformat(results)
    outfile.write(text)
