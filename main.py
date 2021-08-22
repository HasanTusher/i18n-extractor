import json
import re
from collections import OrderedDict
import sys
import os.path

unchanged_count = 0
new_added = 0
total_key = 0


def extractor():
    if len(sys.argv) != 3:
        print('Please provide the valid HTML and Json file tags.')
        return
    if not os.path.exists(sys.argv[1]):
        print('Html File could not be found.')
        return
    if not os.path.exists(sys.argv[2]):
        print('Json File could not be found.')
        return

    file = open(os.path.abspath(sys.argv[1]), 'r')
    file_text = file.read()

    file.close()
    matches = re.findall("\{{\s*[']\s*(.*?)\s*[']\s*[|]\s*translate\s*}}", file_text)
    matches2 = re.findall("[\"]\s*[']\s*(.*?)\s*[']\s*[|]\s*translate\s*[\"]", file_text)

    matches = matches + matches2
    with open(os.path.abspath(sys.argv[2])) as json_en:
        data = json.load(json_en, object_pairs_hook=OrderedDict)
        json_en.close()
        for match in matches:
            data = recur_writer(data, match)

    with open(os.path.abspath(sys.argv[2]), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print('--------Extraction Completed------------')
    print('Extracted File = {}'.format(sys.argv[1]))
    print('Extracted To = {}'.format(sys.argv[2]))
    print('Total Key found = {}'.format(len(matches)))
    print('Unchanged = {}'.format(unchanged_count))
    print('Newly added = {}'.format(new_added))
    print('----------------------------------------')


def recur_writer(obj, matcher):
    exploded_matcher = matcher.split('.')
    temp = obj
    for i, key in enumerate(exploded_matcher):
        if i == len(exploded_matcher)-1:  # last element
            if temp.get(key) is not None:
                global unchanged_count
                unchanged_count += 1
                break
            else:
                global new_added
                new_added += 1
                temp[key] = ""
        else:
            if temp.get(key) is not None:
                temp = temp.get(key)
            else:
                temp[key] = {}
                temp = temp.get(key)

    return obj


extractor()
