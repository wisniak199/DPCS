import json
import sys
import difflib
import re

def similarity(a,b):
    astr = a['crash_report']['stderr_output']
    bstr = b['crash_report']['stderr_output']
    seq=difflib.SequenceMatcher(a=astr.lower(), b=bstr.lower())
    return seq.ratio()

def cluster(json_obj):
    groups = [0] * (len(json_obj) + 1)
    group_counter = 0

    for obj in json_obj:
        id = obj['crash_report']['crash_report_id']
        if (groups[id] != 0):
            continue
        group_counter += 1
        groups[id] = group_counter

        for obj2 in json_obj:
            id2 = obj2['crash_report']['crash_report_id']
            
            if (groups[id2] != 0):
                continue
            
            if (similarity(obj, obj2) > 0.8):
                groups[id2] = group_counter

    for obj in json_obj:
        id = obj['crash_report']['crash_report_id']
        obj['crash_report']['crash_group_id'] = groups[id]

    return json_obj


if __name__ == '__main__':
    json_string = unicode(sys.stdin.read(), errors='ignore')
    json_obj = json.loads(json_string)  
    json_obj = cluster(json_obj)
    print(json_obj)
