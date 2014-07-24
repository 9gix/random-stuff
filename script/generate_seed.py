import re
import os

indirs = os.listdir('input')

for i in indirs:
    outfile = i
    f = open('input/'+i, 'r', encoding='utf16')
    content = f.read()

    pattern = re.compile(r"""
        ^SHOW.\s+(?P<title>.*?)\n
        \s+(?P<description>.*?)\s+
        OWNER.\s+(?P<owner>.*?)\s+$
        .*?
        ^LENGTH.\s+(?P<length>.*?)\s+$
    """, re.MULTILINE|re.DOTALL|re.VERBOSE|re.UNICODE)

    result = pattern.findall(content)

    results = []
    for match in result:

        title = match[0]
        description = ' '.join(x.strip() for x in match[1].splitlines())
        owner = match[2]
        length = match[3]

        vid = {
            'title': title,
            'description': description,
            'owner': owner,
            'length': length,
            'entry_id': "",
            'largeimagepath': "",
        }
        results.append(vid)

    import json
    import pprint

    with open('output/' + outfile, 'w') as outfile:
        pp = pprint.PrettyPrinter(indent=4)
        text = pp.pformat(results)
        text = re.sub(r"'(?P<key>\w+)':", ":\g<key> =>", text)
        outfile.write(text)


